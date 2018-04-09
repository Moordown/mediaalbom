# -*- coding: utf-8 
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import imWindow as imWin
import itertools


class MyScrollArea(QtWidgets.QScrollArea):

    def __init__(self, parent=None, img_size=(240, 240),
                 line_size=5, start_lines=7, upload_lines=7):
        super().__init__(parent)       
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self._w, self._h = img_size  
        self.line_size = line_size  
        self.start_lines = start_lines
        # в wheelEvent заходит два раза, не знаю почему, поэтому здесь делим пополам
        self.upload_lines = upload_lines // 2 if upload_lines > 1 : 1
    
    def upload(self, path):
        """Функция, загружающа названия картинок из поддирректории
        во внутреннюю переменную"""
        self.layout = QtWidgets.QGridLayout()
        self.box = QtWidgets.QWidget()
        self.box.setLayout(self.layout)   
        self.row_num = 0
        self.setWidget(self.box)
        self.img_names = imWin.get_files_from(imWin.EXTENTIONS, path) 
        self.scroll_bar = self.verticalScrollBar()
        self.cur_image_widget = None
        self.last_image_widget = None 
        
        self.cur_slider_position = 0
        self.last_slider_position = 0 
        
        for _ in range(self.start_lines):
            self.add_images()
            self.row_num += 1
    
    def shift_scroll_bar(self):
        self.scroll_bar.setValue(self.scroll_bar.value() + 1)
        
    def wheelEvent(self, event):
        print(type(event))
        self.cur_slider_position = self.scroll_bar.sliderPosition()            
        if (self.cur_slider_position == self.last_slider_position 
            == self.scroll_bar.maximum() and event.angleDelta().y() < 0):
            print('зашли')
            for _ in range(self.upload_lines):
                if self.add_images():
                    self.row_num += 1
                    self.shift_scroll_bar()
            event.accept()
        else:
            event.ignore()
            QtWidgets.QScrollArea.wheelEvent(self, event)
        
        self.last_slider_position = self.cur_slider_position
    
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
            
    def add_images(self):
        """Добавляет картинки в layout пока они есть в поддиректории"""
        self.last_image_widget = self.cur_image_widget
        image_names  = self.take_elements(self.line_size, self.img_names)
        qimages = self.get_scaled_qimages(image_names)
        
        is_first = True
        for i, qimage in enumerate(qimages):
            label = QtWidgets.QLabel()
            label.setFrameShape(QtWidgets.QFrame.Box | QtWidgets.QFrame.Panel)
            label.setPixmap(QtGui.QPixmap.fromImage(qimage))
            label.resize(self._w, self._h)
            if is_first:
                self.cur_image_widget = label
                is_first = False
            self.layout.addWidget(label, self.row_num, i)
            
        return self.last_image_widget != self.cur_image_widget


if __name__ == "__main__":            
    app = QtWidgets.QApplication(sys.argv)
    window = MyScrollArea(img_size=(120, 120), start_lines=2, upload_lines=4)
    window.resize((window.line_size+1) * 120, 200)
    window.show()
    window.upload('.\\images\\')
    sys.exit(app.exec_())
