"""
Module to contain common use functions
"""
import inspect
import ncs
import modules


def build_device_list(input):
    """
    Converts the NSO inputs into a single list of device names
    """
    devices = []
    for item in input.inputs:
        if item.input_type == "device_group":
            with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
                root = ncs.maagic.get_root(trans)
                group = root.devices.device_group[item.value].device_name
                for box in group:
                    if box not in devices:
                        devices.append(box)
        elif item.input_type == "device":
            if item.value not in devices:
                devices.append(item.value)
        elif item.input_type == "csv":
            entries = item.value.split(",")
            for entry in entries:
                if entry not in devices:
                    devices.append(entry)
    return devices


def route(group, module, name, devices, output):
    """
    create the factories and audits, then return the object for the appropriate module.
    """
    module_list = create_modules()
    return module_list[group][module].route_action(name, devices, output)

def create_modules():
    """
    Function that builds all available factorys from modules.
    and buidls all audits from the factory objects created.

    It returns a dictionary of all factories and their modules.
    """
    group_list = {}
    facts = inspect.getmembers(modules,
                        lambda m: inspect.ismodule(m))

    for name, _module in facts:
        if "module" in name and "abs" not in name:
            classes = inspect.getmembers(_module,
                                lambda m: inspect.isclass(m) and not inspect.isabstract(m))
            for name, _class in classes:
                if "Abs" not in name:
                    new_class = _class()
                    if new_class.group not in group_list:
                        group_list.update({new_class.group:{}})
                    group_list[new_class.group].update({new_class.name:new_class})
    return group_list
