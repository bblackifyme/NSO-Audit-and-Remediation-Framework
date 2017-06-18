# NSO Audit & Remediation Framework

> Currently a WORK IN PROGRESS version 0.2

## Package Description

This project contains the framework and source code for developing modular Audit and Remediation code for NSO.

The project provides standardized templates and guidelines for developing a new audit and remediate use case.
It is packages such that a developer or network engineer can easy leverage the templates and simply leverage "Add your code here" sections to add new features. Once complete, the new feature goes through code review and system regression testing before being moved onto prod NSO.

Developers:
Brandon Black branblac@cisco.com

### Development Environment

Developed on: NCS-4.4

NO NED Dependencies

## Usage

This page provides developer and NSO interface usages. For end-user usage, there is an intended CLI "Audit API" project for easy usage that can be executed from a users local machine for easy access to getting Audit results.

The package enforces a standard interface for all audit and remediation use cases. Each use case will have two main actions that can be executed, `audit` and `remediate`. The inputs into the packages will also have an enforced structure. The current input structure is in design phase but is expected to be options between single device, device group, or comma separated device lists.

Output includes time started, ended, run time, results and percent passed.

The results field is to be a standardized form - TBD per design
EXAMPLES:

### CLI example
*TO BE UPDATED*

CLI example to view available audits and remediations:

```bash
branblac@ncs# Audits ?
Possible completions:
  IPv6
```


### REST Payload
*TO BE UPDATED*

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

The documentation in this README provides details into the packages workings, for documentation on developing a new feature or use case please see the contribution guide (link to be added)

### YANG Model

#### Model Logic

The Framework Yang consists of 3 pieces.

1. `audit.yang` - Wrapper model for all audits. New use cases need to be added into this YANG to register them in NSO.
2. `input_output.yang` - Yang grouping to enforce standard input and output fields for all use cases

3. `your_audit_name_here.yang` - Template (ie name changes) that registers the new use case audit & remediate actions into the framework. Imports and uses the `input_output.yang` model.


### Code Logic

The Python directory of the project contains the framework code and use case code.

The framework is contained inside `action.py` and is the code that is registered inside NSO. When audits & remediations are called this module is called.

Inside the `cb_action` method of the `ActionHandler` class is where the user module is registered.

We register the user code by adding an elif block to check what use case is being called. We do this by checking the keypath of the request:

```python
if str(kp) == "/audits:Audits/IPv6":
        output = ipv6.ipv6(self, kp, input, name, output)
```

This example is checking for the "IPv6" use case. We then set the output to the returned output object from the use case code. The use case takes the input and executes its audit or remediate functions per the use case requirements and sets the results.

Once complete. The results are returned to NSO and returned to the user.
