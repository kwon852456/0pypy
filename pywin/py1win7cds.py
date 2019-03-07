
from PyQt5.QtWidgets import *
from PyQt5 import uic
import ctypes.wintypes
import ctypes, ctypes.wintypes, sys
import py1win0 as win0



class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.LPARAM),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.c_void_p)
    ]
PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)


form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("MainWindow")

    def nativeEvent(self, eventType, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if eventType == "windows_generic_MSG":
            if msg.message == 74:
                print(msg.lParam)
                pCDS = ctypes.cast(msg.lParam, PCOPYDATASTRUCT)
                print("dwData=%d cbData=0x%x lpData=0x%x" % (pCDS.contents.dwData, pCDS.contents.cbData, pCDS.contents.lpData))

                yHdr = ctypes.string_at(pCDS.contents.lpData,255)
                stringToReturn = win0.s_yHdr(yHdr)
                QMessageBox.about(self,"message", stringToReturn.decode("utf-8"))


        return False, 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()