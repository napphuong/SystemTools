#! /usr/bin/env python
# -*- coding: utf-8 -*-

import platform
if platform.system() == "Windows":
    import qt_windows
    import synctime
    synctime.synctime()
elif  platform.system()=="Linux":
    print ("Linux is not supported yet!")
