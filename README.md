# NSO Audit & Remediation Framework


## Package Description

This project contains the framework and source code for developing modular Audit and Remediation code for NSO.

The project provides standardized templates and guidelines for developing a new audit and remediate use case.
It is packages such that a developer or network engineer can easy leverage the templates and simply leverage "Add your code here" sections to add new features.

Developers:
Brandon Black bblackifyme@gmail.com

### Development Environment

Developed on: NCS-4.4

NO NED Dependencies

## Usage

This page provides developer and NSO interface usages. For end-user usage, there is an intended CLI "Audit API" project for easy usage that can be executed from a users local machine for easy access to getting Audit results.

The package enforces a standard interface for all audit and remediation use cases. Each use case will have two main actions that can be executed, `audit` and `remediate`. The inputs into the packages will also have an enforced structure. The current input structure is in design phase but is expected to be options between single device, device group, or comma separated device lists.

Output includes time started, ended, run time, results and percent passed.

results returned are a list type with fields of: device_name, result (True = compliant, False = non-compliant),
EXAMPLES:

### CLI example

CLI example to view available audits and remediations:

```
branblac@ncs# Audits ?
Possible completions:
  IPv6

branblac@ncs# Audits IPv6 ?
Possible completions:
  igmp   audit to check that ip igmp v3 set on VLAN 10 and gi0/0/0.10
```


### REST Payload

REST example to execute audits and remediations:

View the available Audits:

GET: `nso-server:8888/api/running/Audits`

Result:
```json
{
    "Audits:Audits": {
        "IPv6": {
            "igmp": {
                "operations": {
                    "audit": "/api/running/Audits/IPv6/igmp/_operations/audit",
                    "remediate": "/api/running/Audits/IPv6/igmp/_operations/remediate"
                }
            },
            "L3_ip_pim": {
                "operations": {
                    "audit": "/api/running/Audits/IPv6/L3_ip_pim/_operations/audit",
                    "remediate": "/api/running/Audits/IPv6/L3_ip_pim/_operations/remediate"
                }
            }
        }
    }
}
```


## Development Documentation

The documentation in this README provides details into the packages workings, for documentation on developing a new feature or use case please see the contribution guide in the docs folder.

### YANG Model

#### Model Logic

The Framework Yang consists of 3 pieces.

1. `audit.yang` - Wrapper model for all audits. New use cases need to be added into this YANG to register them in NSO.
2. `input_output.yang` - Yang grouping to enforce standard input and output fields for all use cases
3. `your_audit_name_here.yang` - Template (ie name changes) that registers the new use case audit & remediate actions into the framework. Imports and uses the `input_output.yang` model.


### Code Logic

The Python directory of the project contains the framework code and use case code.

The framework is contained inside `action.py` and is the code that is registered inside NSO. When audits & remediations are called in NSO this module is executed.

Inside the `cb_action` method of the `ActionHandler` class is where the user modules are dynamically registered. NSO will determine which audit module was called and then route that to a object with the methods defined by the creator for that audit. ie what config needs to be audited.

The objects are created using a simple factory pattern. The factory loops over all the concrete classes present in the modules package(folder) and creates an object of that class. Then adds it to a nested dictionary that has the structure of { Group_name : { Module_name : Module_object } }. The group name is determined by the classes self.group attribute.

Then to route a action request from a user NSO just parses the XPATH of where the request was called from to get the group and module names the calls the dictionary keys for that group and module tog et the implemented object.  Then it calls either audit or remediate method of that object depending on what the user selected.

Once complete. The results are returned to NSO and returned to the user.
