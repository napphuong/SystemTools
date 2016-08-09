import os, sys 
from PyQt5 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QWidget): 
    def __init__(self): 
        QtWidgets.QWidget.__init__(self) 
         
        self.setGeometry(0,0, 500,650) 
        self.setWindowTitle("Debreate") 
        self.setWindowIcon(QtGui.QIcon("icon.png")) 
        self.resize(500,650) 
        self.setMinimumSize(500,650) 
        self.center() 
         
        # --- Menu --- # 
        open = QtWidgets.QAction("Exit", self) 
        save = QtWidgets.QAction("Save", self) 
        build = QtWidgets.QAction("Build", self) 
        exit = QtWidgets.QAction("Quit", self) 
         
        menu_bar = QtWidgets.QMenuBar() 
        file = menu_bar.addMenu("&File") 
        help = menu_bar.addMenu("&Help") 
         
        file.addAction(open) 
        file.addAction(save) 
        file.addAction(build) 
        file.addAction(exit) 
         
        tab_widget = QtWidgets.QTabWidget() 
        tab1 = QtWidgets.QWidget() 
        tab2 = QtWidgets.QWidget() 
         
        p1_vertical = QtWidgets.QVBoxLayout(tab1) 
        p2_vertical = QtWidgets.QVBoxLayout(tab2) 
         
        tab_widget.addTab(tab1, "Main") 
        tab_widget.addTab(tab2, "Description") 
         
        button1 = QtWidgets.QPushButton("button1") 
        p1_vertical.addWidget(button1) 
         
        vbox = QtWidgets.QVBoxLayout() 
        vbox.addWidget(menu_bar) 
        vbox.addWidget(tab_widget) 
         
        self.setLayout(vbox) 
     
     
    def center(self): 
        screen = QtWidgets.QDesktopWidget().screenGeometry() 
        size = self.geometry() 
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2) 


app = QtWidgets.QApplication(sys.argv) 
frame = MainWindow() 
frame.show() 
sys.exit(app.exec_())  
