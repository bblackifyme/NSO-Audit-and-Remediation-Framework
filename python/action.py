"""
NCS Action Package example.

Implements a package with actions
(C) 2015 Tail-f Systems
Permission to use this code as a starting point hereby granted

See the README file for more information
"""
from __future__ import print_function
import sys
from datetime import datetime
import time
import ncs
import _ncs
import _ncs.dp
from ncs.dp import Action
from ncs.application import Application
from _namespaces.audit_ns import ns
import helpers

DATE_FORMAT = "%H:%M:%S.%f"


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
        start = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.start_time = time.strftime("%H:%M:%S")
        devices = helpers.build_device_list(input)
        kp_parse = str(kp).split("/")
        group = kp_parse[2]
        module = kp_parse[3]
        helpers.route(group, module, name, devices, output)
        end = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)

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
