#!/usr/bin/env python3
"""
Polyglot v3 DMP XR node server 
Copyright (C) 2021 Ron Morasse

"""
import udi_interface
import sys
import time
from nodes import ctl
from nodes import zone
from nodes import area

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom
polyglot = None
parameters = None
controller = None
configured = False



if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        # Create the controller node
        controller = ctl.Controller(polyglot, 'controller', 'controller', 'DMP')
        #controller = ctl.AreaController(polyglot, 'controller', 'controller', 'DMP')
        # Just sit and wait for events
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)




     


