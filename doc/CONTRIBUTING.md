# Adding a Use Case / Feature

Follow this guide for developing a new use case with in the Audit and Remediation framework.

<br>

<img src="https://cdn.meme.am/cache/instances/folder832/500x/72340832/coffee-pentagram-its-time-to-code.jpg">

<br>


## High Level Steps:
1. [Git clone the repo](#git-clone-the-repo)
2. [Create a new feature branch](#create-a-new-feature-branch)
3. Copy and rename the yang template
4. Modify and save yang file
5. Register the new module in the audit.yang file
5. Copy and rename the python template
6. Modify and save python file
7. Register the new module in the actions.py file
9. Test locally!!!
10. Merge request into master
11. Code review!
12. CI deployment to stage and regression tests
13. CI Deploy to production

## Git clone the repo

`git clone https://wwwin-gitlab-sjc.cisco.com/NWS-NSO-Packages/Audit-and-Remediation-Framework.git`

## Create a new feature branch

Create a new branch that will include your new use case.

Only modify the files for your project! If you remove or modify files and code that is not apart of this guide your development will be **rejected**!

`git branch your_audit_name_here`

## Copy and rename the yang template

Either do this via your laptops UI or via command line. Save the name to the value you will use for all "your_audit_name_here" changes.

Files located at `/Audit-and-Remediation-Framework/src/yang`

Keep the new file in this location.

## Modify and save the yang file

Begin with your renamed use case .yang file:

Follow the instructions in the file and changed the names where instructed.

**IMPORTANT**
Maintain consistency in the "your_audit_name_here" changes. *If you change this name within the different files your module WILL NOT WORK*

```javascript
module your_audit_name_here { // Change this to your audits name, this needs to be the same everywhere
  namespace "http://example.com/your_audit_name_here"; // Change "your_audit_name_here" to your audits name, this needs to be the same everywhere
  prefix your_audit_name_here; // Change this to your audits name, this needs to be the same everywhere

  import tailf-common {
    prefix tailf;
  }
  import input_output {
    prefix input_output;
  }
  grouping your_audit_name_here { // Change this to your audits name, this needs to be the same everywhere
    container your_audit_name_here { // Change this to your audits name, this needs to be the same everywhere
      tailf:info "Add description here";
      container your_sub_module_name_here { // Change this to your sub-use-cases name copy this for each new use case
        tailf:info "Add description here";
        uses input_output:input_output;
      }
      container your_sub_module_2_name_here { // Change this to your second sub-use-cases name copy this for each new use case
        tailf:info "Add description here";
        uses input_output:input_output;
      }

      }
    }
  }
```

Save the file.

## Register the new module in the audit.yang file

Open up the `audit.yang` file. **DO NOT RENAME THIS FILE**

> IMPORTANT! **DO NOT** change anything not instructed to do in this guide. Any modules with extra changes **WILL BE REJECTED AT CODE REVIEW**

Follow the instructions in the files comments, using ipv6 as an example use case that has been completed.

```javascript
// Please note, DO NOT CHANGE ANYTHING OTHER THAN ADDING YOUR LINES.
// If changes are made there will be "merge conflicts" and you will have to correct what you did!

module Audits {
  namespace "http://example.com/actions";
  prefix audits;

  import tailf-common {
    prefix tailf;
  }
  import ipv6 { prefix ipv6; }

  // import your_audit_name_here { prefix your_audit_name_here; }
  // Add the above line but replace "your_audit_name_here" with your audits name. BE CONSISTENT

  description "Module to store audit actions";

  container Audits {
    uses ipv6:ipv6;

    // uses your_audit_name_here:your_audit_name_here;
    // Add the above line but replace "your_audit_name_here" with your audits name. BE CONSISTENT
  }
}
```

Save the file.

## Copy and rename the python template

Either do this via your laptops UI or via command line. Save the name to the value you will use for all "your_audit_name_here" changes.

Files located at `/Audit-and-Remediation-Framework/python/`

Keep the new file in this location.

## Modify and save the python file

Add your audit code! This is where you have freedom to build your code as you desire to do what it is you think it needs to do!

However, there are a few requirements ;)

1. You must use doc-strings!
2. You must have an "audit" and "remediate" function (this is for readability and consistency, but feel free to call other functions).
3. Please comment, others might not know what you are doing.
4. Follow the module doc-string format. Feel free to add after, but you must include it.

A transaction into the NSO cDB, timers, and total run time calculations is pre-created in the template for you for both audits and remediations:

```python
if name == "audit":
      start = (datetime.strptime(str(datetime.now().time()), date_format))
      output.start_time = time.strftime("%H:%M:%S")
      with ncs.maapi.single_write_trans("ncsadmin",'python',["ncsadmin"],ip='127.0.0.1', port=ncs.NCS_PORT,path=None, src_ip='127.0.0.1', src_port=0, proto=ncs.PROTO_TCP) as t:
              root = ncs.maagic.get_root(t)
              #
              # Your code goes here
              #
      output.result = "Your results here"
      end = (datetime.strptime(str(datetime.now().time()), date_format))
      output.end_time = time.strftime("%H:%M:%S")
      output.run_time = str(end-start)
      output.success_percent = "100%" #CHANGE to your success metric
```

The template is for quick starting, Code Review WILL NOT enforce the use of this structure, but will involve detailed review.

## Register the new module in the actions.py file

actions.py is the main entry for NSO into the framework. The input object passed into it provides details into which use-case and sub-use-case is being called. We need to register and map our new use case in this file so that NSO knows when to run our new code.

Start by importing the python module (file) that you just updated into the actions.py module (ipv6 is an example):

```python
from __future__ import print_function
import sys
import ipv6

# import your_audit_name_here # Copy and change this to the name of your Python File
```


Now we are ready to map the our code to the action inside NSO. We do this by checking the "Keypath" of the triggered event. NSO provides us the keypath as an input into the ActionHandler class where the mapping is done:

```python
class ActionHandler(Action):
    """This class implements the dp.Action class."""

  @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        """Called when the actionpoint is invoked.

        The function is called with:
            uinfo -- a UserInfo object
            name -- the tailf:action name (string)
            kp -- the keypath of the action (HKeypathRef)
            input -- input node (maagic.Node)
            output -- output node (maagic.Node)
        """
        #TODO determine logging standards

        if "/audits:Audits/IPv6" in str(kp):
            output = ipv6.ipv6(self, kp, input, name, output)
        else:
            # Log & return general failures
            self.log.debug("got bad operation: {0}".format(name))
            return _ncs.CONFD_ERR

        ##################################################################
        #                                                                #
        #   To add your feature/use case copy the code snippet below.    #
        #   Add it below the last elif and above the else.               #
        #   Uncomment the block and follow the # commented instructions. #
        #                                                                #
        ##################################################################
        """
        elif str(kp) == "/audits:Audits/your_audit_name_here":
            # Change "your_audit_name_here" to the name of the function inside your new python file
            output = your_audit_name_here.your_audit_name_here(self, kp, input, name, output)
            # Change the first "your_audit_name_here" to the name of your python file, & "your_audit_name_here" to the function name
        """

```

We register our new use case by following the instructions inside the template.

**REMEMBER TO BE CONSISTENT with your_audit_name_here naming. **

Save the file.

***CONGRATULATIONS! You have just built a Audit-and-Remediation-Framework module! Now, its time to test our work!***

## Test locally!!!

Easily the most important and time consuming step!

Before you submit your code to be merged into the master branch (ie running in production) you must test the module locally! Showing a working instance of the code will be required prior to your module being deployed into production.

If you have a local install running place the `Audit-and-Remediation-Framework` package into your packages directory of the running directory of your NSO.

Then cd into the src dir and run `make`, you should see 0 compile errors. If there are errors in the make, then you need to debug and resolve the issues. Odds are, there are `your_audit_name_here` that were not changed, or were changed inconsistently.

Next, log into you NSO CLI `ncs_cli -C` and issue a `packages reload` again, the package should not produce errors. If so, debug the yang.

```bash
branblac@ncs# branblac@ncs# packages reload
reload-result {
    package audit_and_remediate
    result true
}
```

You are now ready to test your code functionality! Use your preferred method, CLI is given.

```shell
branblac@ncs# Audits ?                                 
Possible completions:
  IPv6   IPv6 related audits
branblac@ncs# Audits IPv6 ?
Possible completions:
  L3_ip_pim   
  igmp        audit to check that ip igmp v3 set on VLAN 10 and gi0/0/0.10
branblac@ncs# Audits IPv6 igmp ?
Possible completions:
  audit       Audit
  remediate   Remediation for the use case.
branblac@ncs# Audits IPv6 igmp audit ?
Possible completions:
  Device_group   Audit for the use case.
branblac@ncs# Audits IPv6 igmp audit Device_group dt_gw
start_time 23:00:44
end_time 23:00:44
run_time 0:00:00.038511
result Non-compliant devices: ['demo-0', 'demo-1']
success_percent 0.0
```
