#import os
#os.chdir ("./")

from distutils.core import setup
import py2exe
from glob import glob

includes = ['sip','PyQt4.QtCore']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']

data_files = [
    ('',['config.ini',]),
    ('icon', glob(r'.\icon\*.*'))
]

dist_dir = 'dist'

script = [
    {'script':'system_tools.pyw',
     'icon_resources': [(1, './icon/system_tools.ico')],
    }
]

setup(
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
