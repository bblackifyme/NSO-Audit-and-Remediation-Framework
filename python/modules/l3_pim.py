from .abs_audit import AbsAudit

class L3Pim(AbsAudit):
    
    def __init__(self):
        self.group = "IPv6"

    def audit(self, devices, output):
        print (self.name, " is auditing")

    def remediate(self, devices, output):
        print (self.name, " is remediating")
