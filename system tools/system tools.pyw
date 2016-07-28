#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module create window and buttons in Windows.
"""

from PyQt5 import QtGui, QtCore, QtWidgets
import sys, subprocess, time, configparser
from scripts import windowexists, turnoff, synctime, textbox


DETACHED_PROCESS = 0x00000008
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.button_width = 120
        self.button_height = 30
        self.left_margin = 15
        self.top_margin1 = 35
        self.top_margin2 = 15
        self.timer_update = 100

        # The QWidget widget is the base class of all
        # user interface objects in PyQt4.
        QtWidgets.QMainWindow.__init__(self)
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
        self.minimizeAction = QtWidgets.QAction("Mi&nimize", self,
                triggered=self.showMinimized)

        self.maximizeAction = QtWidgets.QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QtWidgets.QAction("&Restore", self,
                triggered=self.showNormal)
        
        self.exitAction = QtWidgets.QAction(QtGui.QIcon('./icon/logout.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+E')
        self.exitAction.triggered.connect(self.close)

    def createMenuBar (self):        
        # --- Menu --- #       
        # Create main menu
        self.mainMenu = QtWidgets.QMenuBar(self)
        self.fileMenu = self.mainMenu.addMenu('&File')
        
        # Add sub menu
        self.fileMenu.addAction(self.minimizeAction)
        self.fileMenu.addAction(self.maximizeAction)
        self.fileMenu.addAction(self.restoreAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

    def createTrayIcon(self):
        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.exitAction)

        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon('./icon/system_tools.png'))
        self.trayIcon.setToolTip ('System Tools by Napphuong')
        self.trayIcon.setVisible(True)      
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.iconActivated)
    
    def iconActivated(self, reason):
        if reason in (QtWidgets.QSystemTrayIcon.Trigger, QtWidgets.QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                
    def createButtons (self):        
        # --- Button --- #                
        # Create textbox
        self.tbShutdownDelayTime = textbox.MyLineEdit(CONFIG_FILE,'settings','shutdown_time',self)
        self.tbShutdownDelayTime.resize(self.button_width, self.button_height)
        self.tbShutdownDelayTime.move(self.left_margin, self.top_margin1)
        self.tbShutdownDelayTime.setToolTip ('Type delay time for shutdown or restart!')
  
        # add button shutdown after a secified time in textbox
        self.btnShutdown = QtWidgets.QPushButton('SHUTDOWN', self)
        self.btnShutdown.setToolTip('Click to Shutdown!')
        self.btnShutdown.clicked.connect(lambda:subprocess.Popen
                (["shutdown", "-s", "-t", self.tbShutdownDelayTime.text(), "-f"],creationflags=DETACHED_PROCESS))
        self.btnShutdown.resize(self.button_width,self.button_height)
        self.btnShutdown.move(self.left_margin, self.top_margin1 +
                self.top_margin2 + self.button_height)

        # Add a button: restart
        self.btnRestart = QtWidgets.QPushButton('Restart', self)
        self.btnRestart.setToolTip('Click to Restart!')
        self.btnRestart.clicked.connect(lambda: subprocess.Popen \
                (["shutdown", "-r", "-t", self.tbShutdownDelayTime.text()],creationflags=DETACHED_PROCESS))
        self.btnRestart.resize(self.button_width,self.button_height)
        self.btnRestart.move(self.left_margin, self.top_margin1 + 2 * \
                (self.top_margin2 + self.button_height))

        # Cancel shutdown
        self.btnCancelShutdown = QtWidgets.QPushButton('CANCEL SHUTDOWN', self)
        self.btnCancelShutdown.setToolTip('Click to cancel Shutdown!')
        self.btnCancelShutdown.clicked.connect(lambda:subprocess.Popen \
                                               (["shutdown", "-a"],creationflags=DETACHED_PROCESS))
        self.btnCancelShutdown.resize(self.button_width,self.button_height)
        self.btnCancelShutdown.move(self.left_margin, self.top_margin1 + 3 * \
                                    (self.top_margin2 + self.button_height))

        # screen off
        self.btnScreenOff = QtWidgets.QPushButton('&OFF SCREEN', self)
        self.btnScreenOff.setToolTip('Click to turn off screen!')
        self.btnScreenOff.clicked.connect(turnoff.turnoff)
        self.btnScreenOff.resize(self.button_width,self.button_height)
        self.btnScreenOff.move(self.left_margin, self.top_margin1 + 4 * \
                                    (self.top_margin2 + self.button_height))

        # Create progressBar. 
        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.resize(self.button_width * 2 + 50, self.button_height /3)   
        self.progressbar.setValue(0)
        self.progressbar.move(self.left_margin, self.top_margin1 + 5 * \
                      (self.top_margin2 + self.button_height))
        
        # Add run my apps button
        self.btnRunApp = QtWidgets.QPushButton('&Start all apps', self)
        self.btnRunApp.setToolTip('Click to run my favourite apps!')
        self.btnRunApp.clicked.connect(lambda: self.runAppsInConfigFile('app'))
        self.btnRunApp.resize(self.button_width,self.button_height)
        self.btnRunApp.move(self.left_margin *2 + self.button_width, self.top_margin1)
        
        # Add button to add apps
        self.btnAddApp = QtWidgets.QPushButton('Add', self)
        self.btnAddApp.setToolTip('Click to add my favourite apps!')
        self.btnAddApp.clicked.connect(lambda: self.addApps2ConfigFile('app'))
        self.btnAddApp.resize(self.button_width,self.button_height)
        self.btnAddApp.move(self.left_margin *2 + self.button_width, \
                            self.top_margin1 + self.top_margin2 + self.button_height)

        # Create combobox
        self.comboChangePowerPlan = QtWidgets.QComboBox(self)
        self.comboChangePowerPlan.setToolTip('Click to change power option mode!')
        self.comboChangePowerPlan.addItem("Power Saving")
        self.comboChangePowerPlan.addItem("High Performance")
        self.comboChangePowerPlan.resize(self.button_width, self.button_height)
        self.comboChangePowerPlan.move(self.left_margin *2 + self.button_width, \
                                 self.top_margin1 + 2 * (self.top_margin2 + self.button_height))
        self.comboChangePowerPlan.activated.connect(self.changePowerPlan)

        # sync time
        self.btnSyncTime = QtWidgets.QPushButton('SYNC TIME', self)
        self.btnSyncTime.setToolTip('Click to sync time!')
        self.btnSyncTime.clicked.connect(synctime.synctime)
        self.btnSyncTime.resize(self.button_width,self.button_height)
        self.btnSyncTime.move(self.left_margin *2 + self.button_width,  self.top_margin1 + 3 * \
                          (self.top_margin2 + self.button_height))

        # Create apps buttons
        config.read(CONFIG_FILE)
        position = 0
        for i in range(5):
            if config.has_option('app', 'key'+str(i)):
                keyValue = config.get('app', 'key'+str(i))
                self.createButton4EachApp (position, keyValue)
                position +=1

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.trayIcon.showMessage('System Tools by Napphuong', 'Running in the background.')  
                self.hide()
                return
        super(QtWidgets.QMainWindow, self).changeEvent(event)
        
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', 
                         quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.trayIcon.hide()
            del self.trayIcon
            sip.setdestroyonexit(False)
        else:
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
        result = QtWidgets.QMessageBox.question \
                 (self, 'Message', "Run a lot of apps. Are you sure?", \
                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  QtWidgets.QMessageBox.Yes)
        if result == QtWidgets.QMessageBox.Yes and config.has_section(app_section):
            for (each_key, each_val) in config.items(app_section):
                subprocess.Popen(each_val,creationflags=DETACHED_PROCESS)
                time.sleep(1) # wait 1 second before opening another one

    def createButton4EachApp(self,position,appPath):
            self.btnApp = QtWidgets.QPushButton(appPath[appPath.rfind("/")+1:appPath.rfind(".")], self)
            self.btnApp.resize(self.button_width,self.button_height)
            self.btnApp.move(self.left_margin * 4 + self.button_width * 2, \
                                self.top_margin1 + self.top_margin2 * position + self.button_height * position)
            self.btnApp.clicked.connect(lambda: subprocess.Popen(appPath))

    def addApps2ConfigFile(self,app_section):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', 'C:\\')
        if filename:
            config.read(CONFIG_FILE)
            if not config.has_section(app_section):
                config.add_section(app_section)
            count = 0
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
    app = QtWidgets.QApplication(sys.argv) 
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())

#synctime.synctime()
