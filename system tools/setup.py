import time, os
import py2exe
from distutils.core import setup
from glob import glob

includes = ['sip','PyQt4.QtCore']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']

data_files = [
    ('icon', glob(r'./icon/*.*'))
]

dist_dir = '../dist/' + time.strftime("%Y%m%d")

if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)
    
script = [
    {'script':'system tools.pyw',
     'icon_resources': [(1, './icon/system_tools.ico')],
    }
]

setup(
    name='TestPubSub',
    description="Script to test pubsub for packaging",
    version="0.1",
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": dist_dir,
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    data_files = data_files,
    windows = script
)
