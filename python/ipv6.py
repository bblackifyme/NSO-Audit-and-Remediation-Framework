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
date_format = "%H:%M:%S.%f"
import ncs

def ipv6(self, kp, input, name, output):
    self.log.info("in v6")
    if name == "audit":
        start = (datetime.strptime(str(datetime.now().time()), date_format))
        output.start_time = time.strftime("%H:%M:%S")
        with ncs.maapi.single_write_trans("ncsadmin",'python',["ncsadmin"],ip='127.0.0.1', port=ncs.NCS_PORT,path=None, src_ip='127.0.0.1', src_port=0, proto=ncs.PROTO_TCP) as t:
                root = ncs.maagic.get_root(t)
                #
                # Code goes here
                #
        output.result = "Worked"
        end = (datetime.strptime(str(datetime.now().time()), date_format))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)
        output.success_percent = "100%" #CHANGE to your success metric

    elif name == "remediate":
        start = (datetime.strptime(str(datetime.now().time()), date_format))
        output.start_time = time.strftime("%H:%M:%S")
        with ncs.maapi.single_write_trans("ncsadmin",'python',["ncsadmin"],ip='127.0.0.1', port=ncs.NCS_PORT,path=None, src_ip='127.0.0.1', src_port=0, proto=ncs.PROTO_TCP) as t:
                root = ncs.maagic.get_root(t)
                #
                # Code goes here
                #
        output.result = "Worked"
        end = (datetime.strptime(str(datetime.now().time()), date_format))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)
        output.success_percent = "100%" #CHANGE to your success metric
        
    return output
