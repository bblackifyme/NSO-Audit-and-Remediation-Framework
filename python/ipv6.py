"""
Title:
    - IPv6
Developed by:
    - Brandon Black branblac@cisco.com,
    - David Laban dalaban@cisco.com,
    - Callum Corneille ccorneil@cisco.com,
    - Jamie McGregor jamcgreg@cisco.com,
    - Elliot Wise elwise@cisco.com

Description:
    - This function set is for IPv6 Desktop Gateway Audit and Remediation.
    The package checks for several key configurations across campus & branch.
    CLI config to check:
    Vlan10 & Gigethernet0/0/0.10 ip igmp version 3


"""

from datetime import datetime
import time
#import sys
import ncs
import helpers

DATE_FORMAT = "%H:%M:%S.%f"


# MAIN function (entry point from NSO)
def ipv6(self, kp, input, name, output):
    """
    Main entry point that is called from action.py
    This function contains the configuration logic per configlet
    """
    start = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
    output.start_time = time.strftime("%H:%M:%S")
    devices = helpers.build_device_list(input)

    if name == "audit":
        if str(kp) == "/audits:Audits/IPv6/igmp":
            igmp_audit(self, devices, output)
        elif str(kp) == "/audits:Audits/IPv6/L3_ip_pim":
            output.result = "L3 ip pim"

    elif name == "remediate":
                #
                # Code goes here
                #
                pass
    # Stop the timer now that all code is run and save end time and calc run time
    end = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
    output.end_time = time.strftime("%H:%M:%S")
    output.run_time = str(end-start)

    return output

def igmp_audit(self, devices, output):
    """
    Function to encapsulate the auditing of igmp version 3 config on VLAN10 in campus and Ge0/0/0.10 in branch
    """
    non_compliant_boxs = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
        root = ncs.maagic.get_root(trans)
        total = round(len(devices), 2)
        for box in devices:
            self.log.info(box)
            try:
                box = root.devices.device[box]
                #self.log.info((input.Device_group))
                # This is to check if VLAN 10 is there. if not we get a key not found error
                # Check if the version is correct
                if box.config.ios__interface.Vlan[10].ip.igmp.version == 3:
                    result = output.results.create()
                    result.result = True
                    result.device = box.name
                    self.log.info(output.results[box].device)
                elif box.config.ios__interface.GigabitEthernet["0/0/0.10"].ip.igmp.version == 3:
                    result = output.results.create()
                    result.result = True
                    result.device = box.name
                else:
                    result = output.results.create()
                    result.result = False
                    result.device = box.name
                    non_compliant_boxs.append(box.name)
            except KeyError:
                # Handle Key error and key error only. The only key based call we make is for VLAN 10
                non_compliant_boxs.append(box)
                result = output.results.create()
                result.result = False
                result.device = box.name

    issue_count = round(len(non_compliant_boxs), 2)
    output.number_audited = int(total)
    output.success_percent = (total-issue_count)/total



def igmp_remediate(input, output):
    """
    Function to encapsulate the remedition of igmp version 3 config on VLAN10 in campus and Ge0/0/0.10 in branch
    """
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
        root = ncs.maagic.get_root(trans)
        group = root.devices.device_group[input.Device_group].device_name
        for gateway in group:
            box = root.devices.device[gateway]
            if 10 in box.config.ios__interface.Vlan:
                if box.config.ios__interface.Vlan[10].ip.igmp.version == 3:
                    pass
                else:
                    #Set the version if it is not for campus
                    box.config.ios__interface.Vlan[10].ip.igmp.version = 3
            elif "0/0/0.10" in box.config.ios__interface.GigabitEthernet:
                if box.config.ios__interface.GigabitEthernet["0/0/0.10"].ip.igmp.version == 3:
                    pass
                else:
                    #Set the version if it is not for branch
                    box.config.ios__interface.GigabitEthernet["0/0/0.10"].ip.igmp.version = 3
        try:
            trans.apply() #commit the change to the network in a transaction
            output.result = "Remediation Successful"
        except:
            output.result = "nope"
            #TODO add code to return error code.
