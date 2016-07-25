#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module create window and buttons in Windows.
"""

import sys, subprocess, time, configparser
from scripts import windowexists, turnoff, admin
from PyQt4 import QtGui

DETACHED_PROCESS = 0x00000008
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()

class MyLineEdit(QtGui.QLineEdit):
    def __init__(self,section,key,parent=None):
        globals () ['section'] = section
        globals () ['key'] = key
        super(MyLineEdit, self).__init__(parent)
        config.read(CONFIG_FILE)
        if config.has_option(section,key):
            self.setText(config.get(section,key))
            
    def focusInEvent(self, e):
        self.selectAll()
        
    def focusOutEvent(self, e):
        self.saveKeyValue()

    def saveKeyValue(self):
        config.read(CONFIG_FILE)
        if not config.has_section(section): config.add_section(section)
        if not config.has_option(section, key) or config.get(section,key) != self.text():
            config.set(section,key,self.text())
            with open(CONFIG_FILE, 'w') as f: config.write(f)      

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        self.button_width = 120
        self.button_height = 30
        self.left_margin = 15
        self.top_margin1 = 35
        self.top_margin2 = 15
        self.timer_update = 100

        # The QWidget widget is the base class of all
        # user interface objects in PyQt4.
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("System Tools by Napphuong") 
        self.setWindowIcon(QtGui.QIcon('./icon/system_tools.png')) 
        self.resize(300,300) 
        self.setMinimumSize(300,300)
        self.setMaximumSize(450,300)
        
        self.createActions()
        self.createMenuBar()
        self.createTrayIcon()
        self.createButtons()

    def setVisible(self, visible):
        '''re-define setVisible
        "visible" holds the status of the MainWindow
        '''
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(MainWindow, self).setVisible(visible)

    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                triggered=self.showNormal)
        
        self.quitAction = QtGui.QAction(QtGui.QIcon('./icon/logout.png'), "&Quit", self)
        self.quitAction.triggered.connect(QtGui.qApp.quit)
        self.quitAction.setShortcut('Ctrl+Q')
        
        self.exitAction = QtGui.QAction(QtGui.QIcon('./icon/logout.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+E')
        self.exitAction.triggered.connect(self.close)

    def createMenuBar (self):        
        # --- Menu --- #       
        # Create main menu
        self.mainMenu = QtGui.QMenuBar(self)
        self.fileMenu = self.mainMenu.addMenu('&File')
        
        # Add sub menu
        self.fileMenu.addAction(self.minimizeAction)
        self.fileMenu.addAction(self.maximizeAction)
        self.fileMenu.addAction(self.restoreAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon('./icon/system_tools.png'))
        self.trayIcon.setToolTip ('System Tools by Napphuong')
        self.trayIcon.setVisible(True)      
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.iconActivated)
    
    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                
    def createButtons (self):        
        # --- Button --- #                
        # Create textbox
        self.tbShutdownDelayTime = MyLineEdit('settings','shutdown_time',self)
        self.tbShutdownDelayTime.resize(self.button_width, self.button_height)
        self.tbShutdownDelayTime.move(self.left_margin, self.top_margin1)
        self.tbShutdownDelayTime.setToolTip ('Type delay time for shutdown or restart!')
  
        # add button shutdown after a secified time in textbox
        self.btnShutdown = QtGui.QPushButton('SHUTDOWN', self)
        self.btnShutdown.setToolTip('Click to Shutdown!')
        self.btnShutdown.clicked.connect(lambda:subprocess.Popen
                (["shutdown", "-s", "-t", self.tbShutdownDelayTime.text(), "-f"],creationflags=DETACHED_PROCESS))
        self.btnShutdown.resize(self.button_width,self.button_height)
        self.btnShutdown.move(self.left_margin, self.top_margin1 +
                self.top_margin2 + self.button_height)

        # Add a button: restart
        self.btnRestart = QtGui.QPushButton('Restart', self)
        self.btnRestart.setToolTip('Click to Restart!')
        self.btnRestart.clicked.connect(lambda: subprocess.Popen \
                (["shutdown", "-r", "-t", self.tbShutdownDelayTime.text()],creationflags=DETACHED_PROCESS))
        self.btnRestart.resize(self.button_width,self.button_height)
        self.btnRestart.move(self.left_margin, self.top_margin1 + 2 * \
                (self.top_margin2 + self.button_height))

        # Cancel shutdown
        self.btnCancelShutdown = QtGui.QPushButton('CANCEL SHUTDOWN', self)
        self.btnCancelShutdown.setToolTip('Click to cancel Shutdown!')
        self.btnCancelShutdown.clicked.connect(lambda:subprocess.Popen \
                                               (["shutdown", "-a"],creationflags=DETACHED_PROCESS))
        self.btnCancelShutdown.resize(self.button_width,self.button_height)
        self.btnCancelShutdown.move(self.left_margin, self.top_margin1 + 3 * \
                                    (self.top_margin2 + self.button_height))

        # screen off
        self.btnScreenOff = QtGui.QPushButton('&OFF SCREEN', self)
        self.btnScreenOff.setToolTip('Click to turn off screen!')
        self.btnScreenOff.clicked.connect(turnoff.turnoff)
        self.btnScreenOff.resize(self.button_width,self.button_height)
        self.btnScreenOff.move(self.left_margin, self.top_margin1 + 4 * \
                                    (self.top_margin2 + self.button_height))

        # Create progressBar. 
        self.progressbar = QtGui.QProgressBar(self)
        self.progressbar.resize(self.button_width * 2 + 50, self.button_height /3)   
        self.progressbar.setValue(0)
        self.progressbar.move(self.left_margin, self.top_margin1 + 5 * \
                      (self.top_margin2 + self.button_height))
        
        # Add run my apps button
        self.btnRunApp = QtGui.QPushButton('&Start all apps', self)
        self.btnRunApp.setToolTip('Click to run my favourite apps!')
        self.btnRunApp.clicked.connect(lambda: self.runAppsInConfigFile('app'))
        self.btnRunApp.resize(self.button_width,self.button_height)
        self.btnRunApp.move(self.left_margin *2 + self.button_width, self.top_margin1)
        
        # Add button to add apps
        self.btnAddApp = QtGui.QPushButton('Add', self)
        self.btnAddApp.setToolTip('Click to add my favourite apps!')
        self.btnAddApp.clicked.connect(lambda: self.addApps2ConfigFile('app'))
        self.btnAddApp.resize(self.button_width,self.button_height)
        self.btnAddApp.move(self.left_margin *2 + self.button_width, \
                            self.top_margin1 + self.top_margin2 + self.button_height)

        # Create combobox
        self.comboChangePowerPlan = QtGui.QComboBox(self)
        self.comboChangePowerPlan.setToolTip('Click to change power option mode!')
        self.comboChangePowerPlan.addItem("Power Saving")
        self.comboChangePowerPlan.addItem("High Performance")
        self.comboChangePowerPlan.resize(self.button_width, self.button_height)
        self.comboChangePowerPlan.move(self.left_margin *2 + self.button_width, \
                                 self.top_margin1 + 2 * (self.top_margin2 + self.button_height))
        self.comboChangePowerPlan.activated.connect(self.changePowerPlan)

        # sync time
        self.btnSyncTime = QtGui.QPushButton('SYNC TIME', self)
        self.btnSyncTime.setToolTip('Click to sync time!')
        self.btnSyncTime.clicked.connect(admin.synctime)
        self.btnSyncTime.resize(self.button_width,self.button_height)
        self.btnSyncTime.move(self.left_margin *2 + self.button_width,  self.top_margin1 + 3 * \
                          (self.top_margin2 + self.button_height))

        # Add a button: Quit
        self.btnQuit = QtGui.QPushButton('&Quit', self)
        self.btnQuit.setToolTip('Click to quit!')
        self.btnQuit.clicked.connect(QtGui.qApp.quit)
        self.btnQuit.resize(self.button_width,self.button_height)
        self.btnQuit.move(self.left_margin *2 + self.button_width,  self.top_margin1 + 4 * \
                          (self.top_margin2 + self.button_height))        

        # Create apps buttons
        config.read(CONFIG_FILE)
        position = 0
        for i in range(1, 5):
            if config.has_option('app', 'key'+str(i)):
                keyValue = config.get('app', 'key'+str(i))
                self.createButton4EachApp (position, keyValue)
                position +=1
                
    def closeEvent(self, event):
        ''' Actions before close
        '''
        super(QtGui.QMainWindow, self).closeEvent(event)
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()
            
    def runProgressBar(self):
        if self.progressbar.value() != 0:
            self.progressbar.reset()
        maxValue = int(self.tbShutdownDelayTime.text())
        onePercent = maxValue/100
        for i in range (0, 20):
            time.sleep(5*onePercent)
            value = self.progressbar.value() + 5
            self.progressbar.setValue(value)

    def runAppsInConfigFile(self, app_section):
        config.read(CONFIG_FILE)
        # Show a message box
        result = QtGui.QMessageBox.question \
                 (self, 'Message', "Run a lot of apps. Are you sure?", \
                  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, \
                  QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes and config.has_section(app_section):
            for (each_key, each_val) in config.items(app_section):
                subprocess.Popen(each_val,creationflags=DETACHED_PROCESS)
                time.sleep(1) # wait 1 second before opening another one

    def createButton4EachApp(self,position,appPath):
            self.btnApp = QtGui.QPushButton(appPath[appPath.rfind("/")+1:appPath.rfind(".")], self)
            self.btnApp.resize(self.button_width,self.button_height)
            self.btnApp.move(self.left_margin * 4 + self.button_width * 2, \
                                self.top_margin1 + self.top_margin2 * position + self.button_height * position)
            self.btnApp.clicked.connect(lambda: subprocess.Popen(appPath))

    def addApps2ConfigFile(self,app_section):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Choose File', 'C:\\')
        if filename:
            config.read(CONFIG_FILE)
            if not config.has_section(app_section):
                config.add_section(app_section)
            count = 1
            while (config.has_option(app_section, 'key' + str(count))):
                count +=1
            config.set(app_section, 'key' + str(count), filename)
            with open(CONFIG_FILE, 'w') as f: config.write(f)

    def changePowerPlan(self):
        if self.comboChangePowerPlan.currentText() == "Power Saving":
            subprocess.Popen(["powercfg", "-s", "SCHEME_MAX"],creationflags=DETACHED_PROCESS)
        elif self.comboChangePowerPlan.currentText() == "High Performance":
            subprocess.Popen(["powercfg", "-s", "SCHEME_MIN"],creationflags=DETACHED_PROCESS)

# Let the hunt begin
import platform
if platform.system() == "Windows" and \
        not windowexists.windowexists('System Tools by Napphuong'):
    app = QtGui.QApplication(sys.argv) 
    frame = MainWindow()
    frame.show() 
    sys.exit(app.exec_())

admin.synctime()
