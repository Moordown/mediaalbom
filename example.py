import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Widget(QWidget):

    def __init__(self, parent= None):
        super(Widget, self).__init__()
        self.setFixedHeight(200)

        #Container Widget
        widget = QWidget()
        #Layout of Container Widget
        layout = QGridLayout(self)
        self.row_num = 0
        for _ in range(20):
            btn = QPushButton("test")
            layout.addWidget(btn, self.row_num, 0)
            self.row_num += 1
        widget.setLayout(layout)
        
        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        
        #Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
        
        print('for {}'.format(scroll.verticalScrollBar().maximum()))
        for _ in range(10):
            btn = QPushButton("test2")
            hbox = QHBoxLayout(btn)
            hbox.addWidget(btn)
            layout.addWidget(btn, self.row_num, 0, 1, 2)
            self.row_num += 1
            
        #vertical_clider = scroll.verticalScrollBar()
        #vertical_clider.setMaximum(vertical_clider.maximum() + btn.sizeHint().height() * 10) 
        #print('after {}'.format(vertical_clider.maximum()))       

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = Widget()
    dialog.show()
    
    app.exec_()