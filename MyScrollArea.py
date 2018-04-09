# -*- coding: utf-8 
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import imWindow as imWin
import itertools


class MyScrollArea(QtWidgets.QScrollArea):

    def __init__(self, parent=None, img_size=(240, 240), line_size=5):
        super().__init__(parent)       
        self._w, self._h = img_size  
        self.line_size = line_size  
    
    def upload(self, path):
        self.vbox = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QWidget()
        self.box.setLayout(self.vbox)   
        
        scrollBar = self.verticalScrollBar()
        self.setWidget(self.box)
                 
        self.setWidget(self.box)
        self.img_names = imWin.get_files_from(imWin.EXTENTIONS, path)
        
        self.cur_image_widget = None
        self.last_image_widget = None  
        
    def wheelEvent(self, event):
        scrollBar = self.verticalScrollBar()
        print(scrollBar.sliderPosition(), scrollBar.maximum())            
        if scrollBar.sliderPosition() - event.angleDelta().y() >= scrollBar.maximum():
            if self.add_image():
                self.box = QtWidgets.QGroupBox()
                self.box.setLayout(self.vbox)     
                self.setWidget(self.box)
                self.ensureWidgetVisible(self.cur_image_widget)
                
        event.ignore()
        QtWidgets.QScrollArea.wheelEvent(self, event)
    
    @staticmethod    
    def take_elements(amount, generator):
        res = []
        for el in generator:
            res.append(el)
            amount -= 1
            if amount <= 0:
                break
        return res
    
    def get_scaled_qimages(self, image_names):
        for image_name in image_names:
            qimage = QtGui.QImage(image_name)
            yield qimage.scaled(
                self._w,
                self._h, 
                aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                transformMode=QtCore.Qt.SmoothTransformation)  
            
    def add_image(self):
        self.last_image_widget = self.cur_image_widget
        
        image_names  = self.take_elements(self.line_size, self.img_names)

        qimages = self.get_scaled_qimages(image_names)
        
        hbox = QtWidgets.QHBoxLayout()
        
        is_first = True
        for qimage in qimages:
            label = QtWidgets.QLabel()
            label.setFrameShape(QtWidgets.QFrame.Box | QtWidgets.QFrame.Panel)
            label.setPixmap(QtGui.QPixmap.fromImage(qimage))
            
            label.resize(self._w, self._h)
            
            if is_first:
                self.cur_image_widget = label
                is_first = False
            
            hbox.addWidget(label)
        
        self.vbox.addLayout(hbox)
            
        return self.last_image_widget != self.cur_image_widget


if __name__ == "__main__":            
    app = QtWidgets.QApplication(sys.argv)
    window = MyScrollArea(img_size=(120, 120))
    window.resize((window.line_size+1) * 120, 500)
    window.show()
    window.upload('.\\images\\')
    sys.exit(app.exec_())
