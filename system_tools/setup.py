from distutils.core import setup

import py2exe

import os

os.chdir ("D:\\Dropbox (Personal)\\tools\\system_tools\\system_tools\\")

py2exe_opciones = {'py2exe':{'includes':['sip','PyQt4.QtCore']}}
script = [{'script':'qt_windows.py'}]
setup (windows = script, options=py2exe_opciones)
