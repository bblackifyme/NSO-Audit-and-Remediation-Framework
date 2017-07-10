from .abs_audit import AbsAudit
import ncs

class Igmp(AbsAudit):

    def __init__(self):
        self.group = "IPv6"
        self.name = "igmp"

    def audit(self, devices, output):
        non_compliant_boxs = []
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
            root = ncs.maagic.get_root(trans)
            total = round(len(devices), 2)
            for box in devices:
                box = root.devices.device[box]
                if 10 in box.config.ios__interface.Vlan:
                    # Check if the version is correct if there is a VLAN 10
                    if box.config.ios__interface.Vlan[10].ip.igmp.version == 3:
                        result = output.results.create()
                        result.result = True
                        result.device = box.name
                    else:
                        result = output.results.create()
                        result.result = False
                        result.device = box.name
                # Check Branch config which is on GE 0/0/0.10
                elif "0/0/0.10" in box.config.ios__interface.GigabitEthernet:
                    # Check igmp version
                    if box.config.ios__interface.GigabitEthernet["0/0/0.10"].ip.igmp.version == 3:
                        result = output.results.create()
                        result.result = True
                        result.device = box.name
                    else:
                        result = output.results.create()
                        result.result = False
                        result.device = box.name
                        non_compliant_boxs.append(box.name)
        # Set statistics
        issue_count = round(len(non_compliant_boxs), 2)
        output.number_audited = int(total)
        output.success_percent = (total-issue_count)/total

    def remediate(self, devices, output):
        print self.name, " is remediating"
