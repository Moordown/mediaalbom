from PyQt5.QtWidgets import (QMainWindow, QGroupBox, QFormLayout, QLabel,
                             QScrollArea, QVBoxLayout, QHBoxLayout, QApplication,
                             QAction, qApp, QPushButton, QWidget, QDesktopWidget)
from PyQt5.QtGui import (QPixmap, QImage)
from PyQt5.QtGui import QIcon
import cv2
import imWindow as imWin
import sys
import copy


class Window(QMainWindow):
    
    rows = 10;
    central_cols = 6;
    
    def __init__(self):
        super().__init__()
        self.menu_create()

        self.setCentralWidget(self.get_central_widget())
        self.showFullScreen()

    def menu_create(self):
        exitAct = QAction(QIcon('exit.ico'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)        

    @staticmethod
    def get_central_form(height: int, width: int) -> list():
        central_form = QFormLayout()
        hboxes = [QHBoxLayout() for _ in range(Window.rows)]

        for i, im in enumerate(imWin.get_resized_images(imWin.IMAGE_PATH[:-2], width, height)):
            label = QLabel('{}'.format(i))
            w, h, b = im.shape
            bytes_per_line = b * w
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            q_img = QImage(im.data, w, h, bytes_per_line, QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(q_img))

            for hbox in hboxes:
                hbox.addWidget(label)
        for hbox in hboxes:
            central_form.addRow(hbox)

        return central_form

    @staticmethod
    def get_scroll_form(central_group_box: QGroupBox, rows=None, cols=None, cell_size=None):
        scroll = QScrollArea()
        scroll.setWidget(central_group_box)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        return scroll

    def get_central_layout(self, rows=None, cols=None, cell_size=None):
        central_group_box = QGroupBox('central group box')
        central_group_box.setLayout(self.get_central_form(cell_size, cell_size))
        layout = QVBoxLayout(self)
        layout.addWidget(self.get_scroll_form(central_group_box, rows, cols, cell_size))
        layout.addWidget(QPushButton("OK"))
        return layout

    def get_central_widget(self):
        r = QDesktopWidget().availableGeometry().right()
        cell_size = r//Window.rows
        cols = Window.central_cols
        
        w = QWidget()
        w.setLayout(self.get_central_layout(cols=cols, cell_size=cell_size))
        w.move(cell_size * 2, cell_size)
        return w


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
