from datetime import datetime

from PyQt6.QtWidgets import QMessageBox

from SignUp.SignUp import Ui_MainWindow
from libs.DataConnector import DataConnector
from libs.JsonFileFactory import JsonFileFactory
from models.User import User


class SignUpExt(Ui_MainWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.users = self.dc.get_all_user()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButton_SignUp.clicked.connect(self.process_signup)
        self.pushButton_Back.clicked.connect(self.go_back)


    def go_back(self):
        self.MainWindow.close()  # Đóng cửa sổ hiện tại
        if self.previous_window:
            self.previous_window.show()

    def process_signup(self):
        try:
            #Step 1: get user input information:
            UserID = self.lineEdit.text()
            UserName = self.lineEdit_UserName.text()
            UserLoginName=self.lineEdit_LoginName.text()
            Password = self.lineEdit_Password.text()
            Email = self.lineEdit_Email.text()
            SignUpDate = datetime.now().strftime("%d/%m/%Y")  # Tự động gán ngày hiện tại
            FanficNumber = 0
            # Step 2: creUSERIDate Object Model
            self.users = self.dc.get_all_user()
            p = User(UserID, UserName, UserLoginName, Password, Email, SignUpDate, FanficNumber)
            index = self.dc.check_existing_user(self.users, p.UserID)
            if index == -1:  # not found-->insert new
                self.users.append(p)
            else:  # found -> update
                self.users[index] = p
            # Step 3: Save all object into Hard disk:
            jff = JsonFileFactory()
            filename = "../dataset/users.json"
            jff.write_data(self.users, filename)
            self.msg = QMessageBox(self.MainWindow)
            self.msg.setWindowTitle("Notification")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setText("Sign Up Successfully! Welcom to our website")
            self.msg.exec()

        except ValueError as e:
            self.msg = QMessageBox(self.MainWindow)
            self.msg.setWindowTitle("Notification")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setText(f"Error: {e}. Please check information again.")
            self.msg.exec()