# -*- coding: utf-8 
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from MyScrollArea import MyScrollArea


class MyMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.scroll_area =  MyScrollArea(img_size=(120, 120), line_size=5)
        self.hbox = QtWidgets.QHBoxLayout()
        self.vboxes = []
        for i in range(3):
            self.vboxes.append(QtWidgets.QVBoxLayout())
            if i == 1:
                scroll_area = MyScrollArea(img_size=(120, 120), line_size=5)
                scroll_area.upload('.\\images\\')
                self.vboxes[i].addWidget(scroll_area, 1)
                self.hbox.addLayout(self.vboxes[i], 4)
            else:
                label = QtWidgets.QLabel("")
                label.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
                
                self.vboxes[i].addWidget(label, 1)
                self.hbox.addLayout(self.vboxes[i], 1)
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.hbox)
        self.setCentralWidget(self.window)
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.resize(QtCore.QSize(center.x(), center.y()))
        self.show()
        


if __name__ == "__main__":            
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())