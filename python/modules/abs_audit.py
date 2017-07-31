import abc

class AbsAudit():
    metaclass=abc.ABCMeta

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def route_action(self, name, devices, output):
        if name == "audit":
            return self.audit(devices, output)
        elif name == "remediate":
            return self.remediate(devices, output)

    @abc.abstractmethod
    def audit(self, devices, output):
        pass

    @abc.abstractmethod
    def remediate(self, devices, output):
        pass
