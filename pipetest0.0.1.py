# -*- coding: utf-8 -*-
import sys
sys.path.append(r"E:\dev\SynologyDrive\rv\py\0.0.1\libr\pywin") #python libr 폴더

import py1win2hnd2mmf as mmf
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("test_window.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_send.clicked.connect(self.btn_send_clicked)
        self.btn_recv.clicked.connect(self.btn_recv_clicked)



    def btn_send_clicked(self):

        if self.tab_send.currentIndex() == 0:
            print(self.edit_send_byte.text())
            self.wmmf.mmf_s(self.edit_send_byte.text())

        elif self.tab_send.currentIndex() == 1:
            print(self.edit_send_uni.text())
            self.wmmf.mmf_ws(self.edit_send_uni.text())

    def btn_recv_clicked(self):
        if self.tab_recv.currentIndex() == 0:
            self.edit_recv_byte.setText( self.rmmf.s_mmf() )

        elif self.tab_recv.currentIndex() == 1:
            self.edit_recv_uni.setText( self.rmmf.ws_mmf() )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

