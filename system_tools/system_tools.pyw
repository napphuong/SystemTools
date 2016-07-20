#! /usr/bin/env python
# -*- coding: utf-8 -*-

import platform

if platform.system() == "Windows":
    import qt_windows

elif  platform.system()=="Linux":
    import qt_linux
