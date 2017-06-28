"""
NCS Action Package example.

Implements a package with actions
(C) 2015 Tail-f Systems
Permission to use this code as a starting point hereby granted

See the README file for more information
"""
from __future__ import print_function
import sys
import ipv6

# import your_audit_name_here # Copy and change this to the name of your Python File
import ncs
import _ncs
import _ncs.dp
from ncs.dp import Action
from ncs.application import Application
from _namespaces.audit_ns import ns

date_format = "%H:%M:%S.%f"

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
        self.log.info(uinfo.addr)
        self.log.info(uinfo.usid)
        self.log.info(uinfo.username)

        output.username = uinfo.username
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



# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------


class Action(Application):
    """This class is referred to from the package-meta-data.xml."""
    # DO NOT CHANGE THIS INFORMATION

    def setup(self):
        """Setting up the action callback.
           This is used internally by NSO when NSO is re-started or packages a reloaded by NSO.
        """
        self.log.debug('action app start')
        self.register_action('audit', ActionHandler, [])
