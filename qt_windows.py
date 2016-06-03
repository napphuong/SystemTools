#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module create window and buttons in Windows.
"""

CONFIG_FILE = 'config.ini'
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 120
LEFT_MARGIN = 15
TOP_MARGIN1 = 35
TOP_MARGIN2 = 15
TIMER_UPDATE = 100

import sys, subprocess, time, configparser
from PyQt4 import QtCore, QtGui
config = configparser.ConfigParser()

class RightClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "File", parent)

        icon = QtGui.QIcon('./icon/logout.png')
        self.quitAction = QtGui.QAction(icon, '&Close', self)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.triggered.connect(parent.close)
        self.addAction(self.quitAction)
'''
class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon("gnomeradio.xpm"))

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

        self.activated.connect(self.onTrayIconActivated)

        class SystrayWheelEventObject(QtCore.QObject):
            def eventFilter(self, object, event):
                if type(event)==QtGui.QWheelEvent:
                    if event.delta() > 0:
                        sendudp("s51153\n")
                    else:
                        sendudp("s53201\n")
                    event.accept()
                    return True
                return False

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def onTrayIconActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            sendudp("s3641\n")

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")

    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        #QtCore.QTimer.singleShot(100, self.welcome)

'''  
class MainWindow(QtGui.QMainWindow):
    
    def closeEvent(self, event):
        ''' Actions before close
        '''
        super(QtGui.QMainWindow, self).closeEvent(event)
        self.save_shutdown_time()
        
    # Create action to save shutdown time
    def save_shutdown_time(self):
        
        '''Save shutdown countdown time.
        '''
        config.read(CONFIG_FILE)
        if not config.has_section('settings'): config.add_section('settings')
        config.set('settings', 'shutdown_time', self.tbShutdownDelayTime.text())
        with open(CONFIG_FILE, 'w') as f: config.write(f)
        
    # Create action to run app for start my apps button
    @QtCore.pyqtSlot(str, str)
    def run_app(self,config_file, app_section):
        '''str, str -> None
        Run program in config_file under app_section
        '''
        config = configparser.ConfigParser()
        config.read(config_file)
        # Show a message box
        result = QtGui.QMessageBox.question \
                 (self, 'Message', "Run a lot of apps. Are you sure?", \
                  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, \
                  QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes and config.has_section(app_section):
            for (each_key, each_val) in config.items(app_section):
                subprocess.Popen(each_val)
                time.sleep(1) # wait 1 second before opening another one
        
    # Create action to get filename using QFileDialog and add to config file
    @QtCore.pyqtSlot(str)
    def add_app(self,app_section):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Choose File', 'C:\\')
        if filename:
            config.read(CONFIG_FILE)
            if not config.has_section(app_section): config.add_section(app_section)
            count = 1
            while (config.has_option(app_section, 'key' + str(count))):
                count +=1
            config.set(app_section, 'key' + str(count), filename)
            with open(CONFIG_FILE, 'w') as f: config.write(f)

    # Change power plan follow combo box
    def power_mode_change(self):
        if self.comboPowerMode.currentText() == "Power Saving":
            subprocess.Popen(["powercfg", "-s", "SCHEME_MAX"])
        elif self.comboPowerMode.currentText() == "High Performance":
            subprocess.Popen(["powercfg", "-s", "SCHEME_MIN"])

    def __init__(self):
        
        # The QWidget widget is the base class of all
        # user interface objects in PyQt4.
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("System Tools by Napphuong") 
        self.setWindowIcon(QtGui.QIcon('./icon/system_tools.png')) 
        self.resize(300,300) 
        self.setMinimumSize(300,300)
        self.setMaximumSize(300,300)

        # Tray
        self.trayMenu = RightClickMenu(self)
        self.sysTray = QtGui.QSystemTrayIcon(self)
        self.sysTray.setIcon(QtGui.QIcon('./icon/system_tools.png'))
        self.sysTray.setToolTip ('System Tools by Napphuong')
        self.sysTray.setVisible(True)      
        self.sysTray.setContextMenu(self.trayMenu)
        
        # --- Menu --- #       
        # Add exit menu button
        self.exitButton = QtGui.QAction(QtGui.QIcon('./icon/logout.png'),\
                                        '&Exit', self)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.triggered.connect(self.close)
        
        # Create main menu
        mainMenu = QtGui.QMenuBar(self)
        fileMenu = mainMenu.addMenu('&File')

        # Add sub menu 
        fileMenu.addAction(self.exitButton)
        
        # --- Button --- #                
        # Create textbox
        self.tbShutdownDelayTime = QtGui.QLineEdit(self)
        self.tbShutdownDelayTime.resize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.tbShutdownDelayTime.move(LEFT_MARGIN, TOP_MARGIN1)
        self.tbShutdownDelayTime.setToolTip ('Type delay time for shutdown or restart!')
        config.read(CONFIG_FILE)
        if config.has_section('settings'): self.tbShutdownDelayTime.setText \
           (config.get('settings', 'shutdown_time'))
   
        # Shutdown after a secified time in textbox
        self.btnShutdown = QtGui.QPushButton('SHUTDOWN', self)
        self.btnShutdown.setToolTip('Click to Shutdown!')
        self.btnShutdown.clicked.connect(self.save_shutdown_time)
        self.btnShutdown.clicked.connect(lambda:subprocess.Popen \
            (["shutdown", "-s", "-t", self.tbShutdownDelayTime.text()]))
        self.btnShutdown.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnShutdown.move(LEFT_MARGIN, TOP_MARGIN1 + \
                              TOP_MARGIN2 + BUTTON_HEIGHT)

        # Add a button: restart
        self.btnRestart = QtGui.QPushButton('Restart', self)
        self.btnRestart.setToolTip('Click to Restart!')
        self.btnRestart.clicked.connect(self.save_shutdown_time)
        self.btnRestart.clicked.connect(lambda:subprocess.Popen \
            (["shutdown", "-r", "-t", self.tbShutdownDelayTime.text()]))
        self.btnRestart.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnRestart.move(LEFT_MARGIN, TOP_MARGIN1 + 2 * \
                             (TOP_MARGIN2 + BUTTON_HEIGHT))

        # Cancel shutdown
        self.btnCancelShutdown = QtGui.QPushButton('CANCEL SHUTDOWN', self)
        self.btnCancelShutdown.setToolTip('Click to cancel Shutdown!')
        self.btnCancelShutdown.clicked.connect(lambda:subprocess.Popen \
                                               (["shutdown", "-a"]))
        self.btnCancelShutdown.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnCancelShutdown.move(LEFT_MARGIN, TOP_MARGIN1 + 3 * \
                                    (TOP_MARGIN2 + BUTTON_HEIGHT))
        
        # Add run my apps button
        self.btnRunApp = QtGui.QPushButton('&Start my apps', self)
        self.btnRunApp.setToolTip('Click to run my favourite apps!')
        self.btnRunApp.clicked.connect(lambda: self.run_app('config.ini', 'app'))
        self.btnRunApp.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnRunApp.move(LEFT_MARGIN *2 + BUTTON_WIDTH, TOP_MARGIN1)

        # Add button to add apps
        self.btnAddApp = QtGui.QPushButton('Add', self)
        self.btnAddApp.setToolTip('Click to add my favourite apps!')
        self.btnAddApp.clicked.connect(lambda: self.add_app('app'))
        self.btnAddApp.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnAddApp.move(LEFT_MARGIN *2 + BUTTON_WIDTH, \
                            TOP_MARGIN1 + TOP_MARGIN2 + BUTTON_HEIGHT)

        # Create combobox
        self.comboPowerMode = QtGui.QComboBox(self)
        self.comboPowerMode.setToolTip('Click to change power option mode!')
        self.comboPowerMode.addItem("Power Saving")
        self.comboPowerMode.addItem("High Performance")
        self.comboPowerMode.resize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.comboPowerMode.move(LEFT_MARGIN *2 + BUTTON_WIDTH, \
                                 TOP_MARGIN1 + 2 * (TOP_MARGIN2 + BUTTON_HEIGHT))
        self.comboPowerMode.activated.connect(self.power_mode_change)

        # Add a button: quit
        self.btnQuit = QtGui.QPushButton('Quit', self)
        self.btnQuit.setToolTip('Click to quit!')
        self.btnQuit.clicked.connect(self.close)
        self.btnQuit.resize(BUTTON_WIDTH,BUTTON_HEIGHT)
        self.btnQuit.move(LEFT_MARGIN *2 + BUTTON_WIDTH,  TOP_MARGIN1 + 3 * \
                          (TOP_MARGIN2 + BUTTON_HEIGHT))        

        # Create progressBar. 
        self.bar = QtGui.QProgressBar(self)
        self.bar.resize(BUTTON_WIDTH * 2 + 50, BUTTON_HEIGHT /3)   
        self.bar.setValue(0)
        self.bar.move(LEFT_MARGIN, TOP_MARGIN1 + 4 * \
                      (TOP_MARGIN2 + BUTTON_HEIGHT))
            
app = QtGui.QApplication(sys.argv) 
frame = MainWindow()
         
frame.show() 
sys.exit(app.exec_()) 
