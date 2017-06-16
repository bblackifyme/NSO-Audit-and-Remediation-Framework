# NSO Audit & Remediation Framework

> Currently a WORK IN PROGRESS version 0.1

## Package Description

This project contains the framework and source code for developing modular Audit and Remediation code for NSO.

The project provides standardized templates and guidelines for developing a new audit and remediate use case.
It is packages such that a developer or network engineer can easy leverage the templates and simply leverage "Add your code here" sections to add new features. Once complete, the new feature goes through code review and system regression testing before being moved onto prod NSO.

Developers:
Brandon Black : branblac@cisco.com

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

CLI example to execute audits and remediations:
```bash
branblac@ncs# Service-Remediation Remediate Service_Name ubvpn disregard_out_of_sync false
start_time 22:39:06
end_time 22:39:08
run_time 0:00:01.874675
result ['rem-test remediation successful.']
```

### REST Payload
*TO BE UPDATED*

REST example to execute audits and remediations:

REST endpoint: `nso-server:8888/api/running/TBD`

POST:
```xml
<input>
<Service_Name>ubvpn</Service_Name>
</input>
```

Result:
```xml
<output xmlns='http://example.com/actions'>
    <start_time>09:11:36</start_time>
    <end_time>09:11:38</end_time>
    <run_time>0:00:01.739125</run_time>
    <result>['rem-test remediation successful.']</result>
    <success_percent>100</success_percent>
</output>
```


## Development Documentation

The documentation in this README provides details into the packages workings, for documentation on developing a new feature or use case please see the contribution guide (link to be added)

### YANG Model

#### Model Logic

To be Updated


#### Model Components

To be updated

### Code Logic

TO be updated.
