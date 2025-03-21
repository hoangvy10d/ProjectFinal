from PyQt6.QtWidgets import QMessageBox, QMainWindow

from Login.LogIn import Ui_MainWindow
from Manager.Manangement.ManagementUserExt import ManagementUserExt
from SignUp.SignUpExt import SignUpExt
from User.UserFunction.UserFunctionExt import UserFunctionExt

from libs.DataConnector import DataConnector


class LogInExt(Ui_MainWindow):
    def __init__(self,data_connector=None):
        super().__init__()
        self.dc = data_connector or DataConnector()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonSignUp.clicked.connect(self.process_signup)

    def process_signup(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = SignUpExt(self.MainWindow)
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()

    def process_login(self):
        dc = DataConnector()
        uid = self.lineEditLoginName.text()
        pwd = str(self.lineEditPassword.text())

        if self.radioButtoUser.isChecked():
            emp = dc.login_user(uid, pwd)
        elif self.radioButtonManager.isChecked():
            emp = dc.login_manager(uid, pwd)
        else:

            self.msg = QMessageBox(self.MainWindow)
            self.msg.setText("Please choose your role (Manager or User)!)")
            self.msg.exec()
            return

        if emp != None:

            if emp == dc.login_user(uid, pwd):
                self.MainWindow.close()  # close login window
                self.mainwindow = QMainWindow()
                self.myui = UserFunctionExt(data_connector=dc)
                self.myui.setupUi(self.mainwindow)
                self.myui.showWindow()

            elif emp == dc.login_manager(uid, pwd):
                self.MainWindow.close()  # close login window
                self.mainwindow = QMainWindow()
                self.myui = ManagementUserExt(manager_name=uid)
                self.myui = ManagementUserExt(self.MainWindow)
                self.myui.setupUi(self.mainwindow)
                self.myui.showWindow()

        else:
            self.msg = QMessageBox(self.MainWindow)
            self.msg.setWindowTitle("Notification")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setText("Cancel Login")
            self.msg.exec()