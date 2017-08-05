"""
CLI for NSO Audit Framework
"""
import sys
import csv
import json
import base64
import click
import requests
from click.testing import CliRunner
from tabulate import tabulate

class Login():
    """
    Login class that collects global login variables.
    """
    def __init__(self):
        self.server = "http://localhost:8080"
        try:
            Decoder = Decode()
            login = Decoder.decode()
            self.username = login[0]
            self.password = login[1]
        except:
            self.username = "Nope"
            self.password = "Wont Happen"

PASS_LOGIN = click.make_pass_decorator(Login, ensure=True)

@click.group()
@PASS_LOGIN
def main(login):
    """
    Command Line tool for runnning the NSO Audit Framework.
    The tool allows you to run available audits loaded into NSO.
    The tool dynamically pulls available audits from NSO.

    Specificy Audits follows the format:
     --group (the audit container) --module (the sub use case to the grouping)

    The tool takes hostname, NSO device group, and csv strings of hostnames for device inputs.

    Please use the set_credentials command for first time use or to update your Password & Username.

    """


@click.option('--username', prompt="Username")
@click.option('--password', prompt=True, hide_input=True)
@main.command()
def set_credentials(username, password):
    """
    Command to set your credentails for the Audit CLI.

    These are used to authenticate into the NSO server for running audits.
    If you do not have NSO access, then you will need to request access to use the CLI.

    Use OnRamp to request access to:
    OnRamp > Unix Servers > IS > Unix Login Shell Access > nwsnsoprd-1
    """
    DECODER = Decode()
    DECODER.encode(username, password)
    click.echo(click.style("""
                 .--------.
                | .------. |
               | /        \ |
               | |        | |
              _| |________| |_
            .' |_|        |_| '.
            '._____ ____ _____.'
            |     .'____'.     |
            '.__.'.'    '.'.__.'
            '.__  |  NSO |  __.'
            |   '.'.____.'.'   |
            '.____'.____.'____.'
            '.________________.'

          Your password has been set\n""", fg="red"))


@main.command()
@PASS_LOGIN
def show_groups(login):
    """
    Command to get the current list of audit groups availalbe to run.
    """
    url = login.server + "/api/running/Audits/"
    headers = {
        'accept': "application/vnd.yang.data+json",
        'cache-control': "no-cache",
        }
    results = requests.request("GET",
                               url, headers=headers,
                               auth=(login.username, login.password))

    data = results.json()
    for each in data["Audits:Audits"]:
        click.echo(each)


@main.command()
@PASS_LOGIN
@click.option('--group', help='Audit to get sub audits for.')
def show_modules(login, group):
    """
    Command to get the current list of modules to run for a provided group.

    Specify the group with --group NAME

    To get list of groups available use the show_groups command
    """
    data = sub_audits_helper(group, login)
    sub_audits = []
    for each in data["Audits:"+str(group)]:
        click.echo(each)
        sub_audits.append(each)

@main.command()
@PASS_LOGIN
def show_device_groups(login):
    """
    Command to get the current list of device groups availalbe to use for audits.
    """
    url = login.server + "/api/running/devices/device-group"
    headers = {
        'accept': "application/vnd.yang.collection+json",
        'cache-control': "no-cache",
        }
    results = requests.request("GET",
                               url, headers=headers,
                               auth=(login.username, login.password))

    data = results.json()
    for each in data["collection"]["tailf-ncs:device-group"]:
        click.echo(each["name"])

@click.option('--device_group', help='Device group to get list of devices for')
@main.command()
@PASS_LOGIN
def show_device_group_devices(login, device_group):
    """
    Command to get the current list of devices for a device group.
    """
    url = login.server + "/api/running/devices/device-group/" + device_group
    headers = {
        'accept': "application/vnd.yang.data+json",
        'cache-control': "no-cache",
        }
    results = requests.request("GET",
                               url, headers=headers,
                               auth=(login.username, login.password))

    data = results.json()
    click.echo("---- Devices ----")
    for each in data["tailf-ncs:device-group"]["device-name"]:
        click.echo(each)
    if data["tailf-ncs:device-group"]["device-group"]:
        click.echo("---- Device Groups ----")
        for each in data["tailf-ncs:device-group"]["device-group"]:
            click.echo(each)


@click.option('--devices', default="nope", help='Input for devices. Format of --device device1, device2, device3 ')
@click.option('--device_group', default="nope", help='Input for device groups. Format of --device_group dg1, dg2, dg3 ')
@click.option('--group', help='Which audit grouping to use')
@click.option('--module', default="all", help='Which module in the group to run')
@click.option('--output', default="table", help="""Options for output.""",type=click.Choice(['table', 'csv_file', 'json']))
@main.command()
@PASS_LOGIN
def run_audit(login, group, module, devices, device_group, output):
    """
    Command to run an audit. This command is flexible and works for any available audit.

    To run an audit on an individual module use: --group GROUP_NAME --module MODULE_NAME

    To run an audit on all modules only include the group name: --group GROUP_NAME
    """
    if devices == "nope" and device_group == "nope":
        click.echo("Please enter devices to be audited!")
    elif module != "all":
        data = audit_rest_call(login, group, module, devices, device_group)
        print data
        #click.echo("Username: " + data[u'Audits:output'][u"username"])
        click.echo("Running time: " + data[u'Audits:output'][u'run_time'])
        click.echo("Compliance Rate: " + data[u'Audits:output'][u'success_percent'])
        click.echo("Number Devices Audited: " + str(data[u'Audits:output'][u'number_audited']))
        table_data = []
        for result in data[u'Audits:output'][u'results']:
            table_data.append([result["device"], str(result["result"])])
        if output == "table":
            click.echo(click.style("************* Audit Results *************", fg="blue"))
            click.echo(click.style(tabulate(table_data, headers=["Module" ,"Device Name", "Compliance"]), fg="red"))
        elif output == "json":
            click.echo(json.dumps(data, indent=4, sort_keys=True))
        elif output == "csv_file":
            with open("audit_output.csv",'wb') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                wr.writerow(["module", "device", "compliance"])
                wr.writerows(table_data)
    elif module == "all":
        table_data = []
        audits = sub_audits_helper(group, login)
        sub_audits = []
        for each in audits["Audits:"+str(group)]:
            sub_audits.append(each)
        with click.progressbar(sub_audits, label='Auditing all modules:', length=len(sub_audits)) as modules:
            for mod in modules:
                data = audit_rest_call(login, group, mod, devices, device_group)
                for result in data[u'Audits:output'][u'results']:
                    table_data.append([mod, result[u"device"], str(result["result"])])

        if output == "table":
            click.echo(click.style("************* Audit Results *************", fg="blue"))
            click.echo(click.style(tabulate(table_data, headers=["Module" ,"Device Name", "Compliance"]), fg="red"))
        elif output == "json":
            click.echo(json.dumps(data, indent=4, sort_keys=True))
        elif output == "csv_file":
            with open("audit_output.csv",'wb') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                wr.writerow(["module", "device", "compliance"])
                wr.writerows(table_data)

    else:
        click.echo("No proper module")



def sub_audits_helper(audit, login):
    """
    Helper to get current list of devices for a audit grouping.
    """
    url = login.server + "/api/running/Audits/"+str(audit)
    headers = {
        'accept': "application/vnd.yang.data+json",
        'cache-control': "no-cache",
        }
    results = requests.request("GET",
                               url, headers=headers,
                               auth=(login.username, login.password))
    data = results.json()
    return data

def audit_rest_call(login, group, module, devices, device_group):
    """
    Function to encapsulate the REST call to get audit data
    """

    url = login.server + "/api/running/Audits/"+str(group)+"/"+str(module)+"/_operations/audit"
    headers = {
        'content-type': "application/vnd.yang.operation+json",
        'cache-control': "no-cache",
        }
    #payload = "\n{\n\t\"input\":{\n\t\t\"inputs\":{\n\t\t\t\"input_type\":\"device\",\n\t\t\t\"value\": \"demo-2\"\n\t\t}\n\t}\n}"
    payload = generate_input_payload(devices, device_group)
    results = requests.request("POST",
                               url, data=payload, headers=headers,
                               auth=(login.username, login.password))
    return results.json()

def generate_input_payload(devices, device_group):
    """
    Helper function to generate the JSON payload for inputs into an audit
    """
    payload = { "input": {"inputs":[]} }
    if devices != "nope":
        devices = devices.split(",")
        for index, device in enumerate(devices):
            device = device.replace(" ", "")
            device = {"input_type":"device","value":device}
            payload["input"]["inputs"].append(device)

    if device_group != "nope":
        device_group = device_group.split(",")
        for index, device_group in enumerate(device_group):
            device_group = device_group.replace(" ", "")
            device_group = {"input_type":"device_group","value":device_group}
            payload["input"]["inputs"].append(device_group)

    return json.dumps(payload)

class Decode(object):
    '''Saves and hides credentials.'''

    def __init__(self, textfile=None):
        '''Determine which file to use for credentials.'''
        if textfile:
            self.textfile = textfile
        else:
            self.textfile = "credentials.txt"

    def encode(self, username, password):
        '''Encodes and saves credentials to textfile.'''
        hidden_user = base64.b64encode(username)
        hidden_pass = base64.b64encode(password)
        with open(self.textfile, "w") as f:
            f.write("{}\n".format(hidden_user))
            f.write("{}\n".format(hidden_pass))

    def decode(self):
        '''Decodes and returns credentials.'''
        with open(self.textfile, "r") as f:
            lines = f.read().splitlines()
            username = base64.b64decode(lines[0])
            password = base64.b64decode(lines[1])
        return (username, password)

if __name__ == '__main__':
    main()

    #runner = CliRunner()
    #result = runner.invoke(main, ['set_credentials',"--username", "admin","--password", "admin"])
    #assert result.exit_code == 0
    #assert 'NSO' in result.output
