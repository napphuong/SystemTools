#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module create window and buttons in Windows.
"""

from PyQt5 import QtGui, QtCore, QtWidgets
import sys, subprocess, time, configparser
from scripts import windowexists, turnoff, synctime, textbox, readpowerplan


DETACHED_PROCESS = 0x00000008
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__() 

        self.setGeometry(0,0, 350,450) 
        self.setWindowTitle("System Tools by Napphuong") 
        self.setWindowIcon(QtGui.QIcon("./icons/system_tools.png")) 
        self.resize(300,300) 
        self.setMinimumSize(300,300) 
        self.center()
        
        self.createActions()
        self.createMenuBar()
        self.createTrayIcon()
        self.createButtons()
        self.createTabs()

        vbox = QtWidgets.QVBoxLayout() 
        vbox.addWidget(self.mainMenu) 
        vbox.addWidget(self.tab_widget) 
         
        self.setLayout(vbox)
        
    def center(self): 
        screen = QtWidgets.QDesktopWidget().screenGeometry() 
        size = self.geometry() 
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    '''   
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            #if self.windowState() & QtCore.Qt.WindowMinimized:
            event.ignore()
            self.trayIcon.showMessage('System Tools by Napphuong', 'Running in the background.')  
            self.hide()
            return
        super(QtWidgets.QtWidgets, self).changeEvent(event)
    '''  
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', 
                         quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.trayIcon.hide()
            del self.trayIcon
            sip.setdestroyonexit(False)
        else:
            self.hide()
            self.trayIcon.showMessage('System Tools by Napphuong', 'Running in the background.')
            event.ignore()
    
    def iconActivated(self, reason):
        if reason in (QtWidgets.QSystemTrayIcon.Trigger, QtWidgets.QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                
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
        
        self.exitAction = QtWidgets.QAction(QtGui.QIcon('./icons/logout.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+E')
        self.exitAction.triggered.connect(self.close)

    def createMenuBar (self):        
        # --- Menu --- #       
        # Create main menu
        self.mainMenu = QtWidgets.QMenuBar(self)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.aboutMenu = self.mainMenu.addMenu('&About')
        
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
        self.trayIcon.setIcon(QtGui.QIcon('./icons/system_tools.png'))
        self.trayIcon.setToolTip ('System Tools by Napphuong')
        self.trayIcon.setVisible(True)      
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.iconActivated)

    def createTabs(self):
        self.tab_widget = QtWidgets.QTabWidget()
        
        tab1 = QtWidgets.QWidget() 
        tab2 = QtWidgets.QWidget() 
        tab3 = QtWidgets.QWidget()
        tab4 = QtWidgets.QWidget()
        
        p1_vertical = QtWidgets.QGridLayout(tab1) 
        p2_vertical = QtWidgets.QVBoxLayout(tab2) 
        p3_vertical = QtWidgets.QVBoxLayout(tab3)
        p4_vertical = QtWidgets.QVBoxLayout(tab4)
         
        self.tab_widget.addTab(tab1, "Shutdown") 
        self.tab_widget.addTab(tab2, "Power") 
        self.tab_widget.addTab(tab3, "Aplication")
        self.tab_widget.addTab(tab4, "Others")
        
        p1_vertical.addWidget(self.tbShutdownDelayTime,0,0) 
        p1_vertical.addWidget(self.btnShutdown,1,0)
        p1_vertical.addWidget(self.btnRestart,2,0)
        p1_vertical.addWidget(self.btnCancelShutdown,3,0)

        p2_vertical.addWidget(self.comboChangePowerPlan)
        p2_vertical.addWidget(self.btnScreenOff)
        p2_vertical.addStretch(1)

        p3_vertical.addWidget(self.btnAddApp)         
        p3_vertical.addWidget(self.btnRunApp)
        # Add apps to p3_vertical
        config.read(CONFIG_FILE)
        for i in range(5):
            if config.has_option('app', 'key'+str(i)):
                keyValue = config.get('app', 'key'+str(i))
                self.createButton4EachApp (p3_vertical, keyValue)
        p3_vertical.addStretch(1)

        p4_vertical.addWidget(self.btnSyncTime)
        p4_vertical.addWidget(self.btnBackupReg)
        p4_vertical.addWidget(self.btnRestoreReg)
        p4_vertical.addStretch(1)
        
    def createButtons (self):        
        # --- Button --- #                
        # Create textbox
        self.tbShutdownDelayTime = textbox.MyLineEdit(CONFIG_FILE,'settings','shutdown_time',self)
        self.tbShutdownDelayTime.setToolTip ('Type delay time for shutdown or restart!')
  
        # add button shutdown after a secified time in textbox
        self.btnShutdown = QtWidgets.QPushButton('SHUTDOWN', self)
        self.btnShutdown.setToolTip('Click to Shutdown!')
        self.btnShutdown.clicked.connect(lambda:subprocess.Popen
                (["shutdown", "-s", "-t", self.tbShutdownDelayTime.text(), "-f"],creationflags=DETACHED_PROCESS))

        # Add a button: restart
        self.btnRestart = QtWidgets.QPushButton('Restart', self)
        self.btnRestart.setToolTip('Click to Restart!')
        self.btnRestart.clicked.connect(lambda: subprocess.Popen \
                (["shutdown", "-r", "-t", self.tbShutdownDelayTime.text()],creationflags=DETACHED_PROCESS))

        # Cancel shutdown
        self.btnCancelShutdown = QtWidgets.QPushButton('CANCEL SHUTDOWN', self)
        self.btnCancelShutdown.setToolTip('Click to cancel Shutdown!')
        self.btnCancelShutdown.clicked.connect(lambda:subprocess.Popen \
                                               (["shutdown", "-a"],creationflags=DETACHED_PROCESS))

        # screen off
        self.btnScreenOff = QtWidgets.QPushButton('&OFF SCREEN', self)
        self.btnScreenOff.setToolTip('Click to turn off screen!')
        self.btnScreenOff.clicked.connect(turnoff.turnoff)

        # Add run my apps button
        self.btnRunApp = QtWidgets.QPushButton('&Start all apps', self)
        self.btnRunApp.setToolTip('Click to run my favourite apps!')
        self.btnRunApp.clicked.connect(lambda: self.runAppsInConfigFile(CONFIG_FILE,'app'))

        # Add button to add apps
        self.btnAddApp = QtWidgets.QPushButton('Add', self)
        self.btnAddApp.setToolTip('Click to add my favourite apps!')
        self.btnAddApp.clicked.connect(lambda: self.addApps2ConfigFile('app'))

        # Create combobox
        self.comboChangePowerPlan = QtWidgets.QComboBox(self)
        self.comboChangePowerPlan.setToolTip('Click to change power option mode!')
        self.comboChangePowerPlan.addItem("Power Saver")
        self.comboChangePowerPlan.addItem("High Performance")
        self.comboChangePowerPlan.addItem("Balanced (recommended)")
        self.comboChangePowerPlan.setCurrentIndex(readpowerplan.readpowerplan())
        self.comboChangePowerPlan.activated.connect(self.changePowerPlan)

        # sync time
        self.btnSyncTime = QtWidgets.QPushButton('SYNC TIME', self)
        self.btnSyncTime.setToolTip('Click to sync time!')
        self.btnSyncTime.clicked.connect(synctime.synctime)

        # backup reg
        self.btnBackupReg = QtWidgets.QPushButton('BACKUP REG', self)
        self.btnBackupReg.setToolTip('Click to back up registry before re-install windows!')
        self.btnBackupReg.clicked.connect(self.backupReg)
 
        # restore reg
        self.btnRestoreReg = QtWidgets.QPushButton('RESTORE REG', self)
        self.btnRestoreReg.setToolTip('Click to restore registry after re-install windows')
        self.btnRestoreReg.clicked.connect(self.restoreReg)

    def backupReg(self):
        subprocess.check_call(r'.\batchs\exportreg.bat',shell=True)
        QtWidgets.QMessageBox.information \
                 (self, 'Message', "Backup Done!", \
                  QtWidgets.QMessageBox.Ok)
                              
    def restoreReg(self):
        subprocess.Popen(['runas', r'/user:administrator' r'.\batchs\importreg.bat'],creationflags=DETACHED_PROCESS)
        QtWidgets.QMessageBox.information \
                 (self, 'Message', "Restore Done!", \
                  QtWidgets.QMessageBox.Ok)
        
    def runAppsInConfigFile(self, config_file, app_section):
        config.read(config_file)
        # Show a message box
        result = QtWidgets.QMessageBox.question \
                 (self, 'Message', "Run a lot of apps. Are you sure?", \
                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, \
                  QtWidgets.QMessageBox.Yes)
        if result == QtWidgets.QMessageBox.Yes and config.has_section(app_section):
            for (each_key, each_val) in config.items(app_section):
                subprocess.Popen(each_val,creationflags=DETACHED_PROCESS)
                time.sleep(1) # wait 1 second before opening another one

    def createButton4EachApp(self, tab, appPath):
            self.btnApp = QtWidgets.QPushButton('&' + appPath[appPath.rfind("/")+1:appPath.rfind(".")], self)
            self.btnApp.clicked.connect(lambda: subprocess.Popen(appPath))
            tab.addWidget(self.btnApp)

    def addApps2ConfigFile(self,app_section):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose File', 'C:\\')
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
        if self.comboChangePowerPlan.currentIndex () == 0:
            subprocess.Popen(["powercfg", "-s", "SCHEME_MAX"],creationflags=DETACHED_PROCESS)
        elif self.comboChangePowerPlan.currentIndex () == 1:
            subprocess.Popen(["powercfg", "-s", "SCHEME_MIN"],creationflags=DETACHED_PROCESS)

#------------------------------------------------------------------------------#
import platform
if platform.system() == "Windows" and \
        not windowexists.windowexists('System Tools by Napphuong'):
    app = QtWidgets.QApplication(sys.argv) 
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())

synctime.synctime()
