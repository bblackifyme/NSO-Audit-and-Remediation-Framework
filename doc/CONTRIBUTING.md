# Adding a Use Case / Feature

Follow this guide for developing a new use case with in the Audit and Remediation framework.

<br>

<img src="https://cdn.meme.am/cache/instances/folder832/500x/72340832/coffee-pentagram-its-time-to-code.jpg">

<br>


## High Level Steps:
1. [Git clone the repo](#git-clone-the-repo)
2. [Create a new feature branch](#create-a-new-feature-branch)
3. [Copy and rename the yang template](#copy-and-rename-the yang-template)
4. [Modify and save yang file](#modify-and-save-yang-file)
5. [Copy and rename the python template](#copy-and-rename-the-python-template)
6. [Modify and save python file](#modify-and-save-python-file)
9. [Test locally!!!](#test-locally!!!)
10. [Merge request into master](#merge-request-into-master)
11. [Code review!](#code-review!)
12. CI deployment to stage and regression tests
13. CI Deploy to production

## Git clone the repo

`git clone https://wwwin-gitlab-sjc.cisco.com/NWS-NSO-Packages/Audit-and-Remediation-Framework.git`

## Create a new feature branch

Create a new branch that will include your new use case.

Only modify the files for your project! If you remove or modify files and code that is not apart of this guide your development will be **rejected**!

`git branch your_audit_name_here`



## For a new audit Group -  Copy and rename the yang template

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
  import Audits {
    prefix audit;
  }

  augment /audit:Audits {
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

## For a new audit module -  Copy and rename the yang template

Since modules belong to audit groups, we can leverage an existing group YANG and just add in a new module:.

Navigate to the appropriate groups .yang file and add the module name and description! Its that easy!

```
container your_sub_module_2_name_here { // Change this to your second sub-use-cases name copy this for each
  tailf:info "Add description here";
  uses input_output:input_output;
}
```


## Copy and rename the python template

Copy and rename the file  "your_module_name_here.py"

Either do this via your laptops UI or via command line.

Follow the naming convention of:
`groupName_moduleName_module.py` the module *MUST* end with `_module.py`


Files located at `/Audit-and-Remediation-Framework/python/modules`

Keep the new file in this location.

## Modify and save the python file

Add your audit code! This is where you have freedom to build your code as you desire to do what it is you think it needs to do!

However, there are a few requirements ;)

1. You must use doc-strings!
2. You must have an "audit" and "remediate" method (this is for readability and consistency, but feel free to call other functions).
3. Please comment, others might not know what you are doing.
4. Follow the module doc-string format. Feel free to add after, but you must include it.

All you have to do is write your audit and remediate methods and populate the output object values!

a note: you need to create your own NSO transaction

```python
from .abs_audit import AbsAudit

class your_module_name_here(AbsAudit):

    def __init__(self):
        self.group = "The group name you used in yang"

    def audit(self, devices, output):
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as trans:
            root = ncs.maagic.get_root(trans)
        """
        Per inputed device add the audit results as follows:

        result = output.results.create()
        result.result = True
        result.device = (device name from input)
        """

    def remediate(self, devices, output):
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as trans:
            root = ncs.maagic.get_root(trans)
            ## Bunch of remediation code here
            trans.apply() ## Apply the changes!
        """
        If your transaction succeeds than we know all devices succeeded :)
        So loop over all inputs and assign as true, or... do a transaction per device (warning, that is very slow!)

        Sample setting output:

        for device in devices:
          result = output.results.create()
          result.result = True
          result.device = (device name from input)
        """
```


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

```
branblac@ncs# Audits IPv6 igmp audit inputs { input_type device value ios-0 } inputs { input_type device value demo-0 }
start_time 20:29:29
end_time 20:29:29
run_time 0:00:00.022778
number_audited 2
results {
    device ios-0
    result false
}
results {
    device demo-0
    result false
}
success_percent 0.0
branblac@ncs#

```
