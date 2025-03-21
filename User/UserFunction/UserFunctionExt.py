from PyQt6.QtWidgets import QMainWindow

from User.ReadFanfic.ReadFanficExt import ReadFanficExt
from User.ReadReview.ReadReviewExt import ReadReviewExt
from User.UserFunction.UserFunction import Ui_MainWindow
from User.WriteFanfic.WriteScriptExt import WriteScriptExt
from libs.DataConnector import DataConnector


class UserFunctionExt(Ui_MainWindow):
    def __init__(self, data_connector=None):
        super().__init__()
        self.dc = data_connector or DataConnector()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonWriteScript.clicked.connect(self.process_WriteScript)
        self.pushButtonReadReview.clicked.connect(self.process_ReadReview)
        self.pushButtonReadFanfic.clicked.connect(self.process_ReadFanfic)

    def process_WriteScript(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = WriteScriptExt(self.MainWindow, data_connector=self.dc )
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()

    def process_ReadReview(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = ReadReviewExt(self.MainWindow)
        self.myui.setupUi(self.mainwindow)
        self.myui.lineEdit_Author.setEnabled(False)
        self.myui.lineEdit_Date.setEnabled(False)
        self.myui.lineEdit_Title.setEnabled(False)
        self.myui.textEdit.setEnabled(False)
        self.myui.showWindow()


    def process_ReadFanfic(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = ReadFanficExt(self.MainWindow)
        self.myui.setupUi(self.mainwindow)
        self.myui.lineEdit_Character.setEnabled(False)
        self.myui.lineEdit_Author.setEnabled(False)
        self.myui.lineEdit_Date.setEnabled(False)
        self.myui.lineEdit_Title.setEnabled(False)
        self.myui.textEdit.setEnabled(False)
        self.myui.showWindow()

