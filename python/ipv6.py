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

DATE_FORMAT = "%H:%M:%S.%f"


# MAIN function (entry point from NSO)
def ipv6(self, kp, input, name, output):
    """
    Main entry point that is called from action.py
    This function contains the configuration logic per configlet
    """
    if name == "audit":
        start = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.start_time = time.strftime("%H:%M:%S")
        self.log.info(str(kp))
        if str(kp) == "/audits:Audits/IPv6/igmp":
            igmp_audit(input, output)
        elif str(kp) == "/audits:Audits/IPv6/L3_ip_pim":
            output.result = "L3 ip pim"
        end = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)
        # output.success_percent = "100%" #CHANGE to your success metric

    elif name == "remediate":
        start = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.start_time = time.strftime("%H:%M:%S")

                #
                # Code goes here
                #
        output.result = "Worked"
        end = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)
        output.success_percent = "100%" #CHANGE to your success metric

    return output

def igmp_audit(input, output):
    """
    Function to encapsulate the auditing of igmp version 3 config on VLAN10 in campus and Ge0/0/0.10 in branch
    """
    non_compliant_boxs = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
        root = ncs.maagic.get_root(trans)
        group = root.devices.device_group[input.Device_group].device_name
        total = round(len(group), 2)
        for gateway in group:
            box = root.devices.device[gateway]
            try:
                # This is to check if VLAN 10 is there. if not we get a key not found error
                # Check if the version is correct
                if box.config.ios__interface.Vlan[10].ip.igmp.version == 3:
                    pass
                elif box.config.ios__interface.GigabitEthernet["0/0/0.10"].ip.igmp.version == 3:
                    pass
                else:
                    non_compliant_boxs.append(box.name)
            except KeyError:
                # Handle Key error and key error only. The only key based call we make is for VLAN 10
                non_compliant_boxs.append(box.name)
    issue_count = round(len(non_compliant_boxs), 2)
    output.success_percent = (total-issue_count)/total
    output.result = "Non-compliant devices: " + str(non_compliant_boxs)

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
