#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from PyQt5 import QtWidgets
config = configparser.ConfigParser()

class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self,config_file,section,key,parent=None):
        globals () ['config_file'] = config_file
        globals () ['section'] = section
        globals () ['key'] = key
        super(MyLineEdit, self).__init__(parent)
        config.read(config_file)
        if config.has_option(section,key):
            self.setText(config.get(section,key))
        else:
            self.setText('0')
    def focusInEvent(self, e):
        self.selectAll()
        
    def focusOutEvent(self, e):
        self.saveKeyValue()

    def saveKeyValue(self):
        config.read(config_file)
        if not config.has_section(section): config.add_section(section)
        if not config.has_option(section, key) or config.get(section,key) != self.text():
            config.set(section,key,self.text())
            with open(config_file, 'w') as f: config.write(f) 
