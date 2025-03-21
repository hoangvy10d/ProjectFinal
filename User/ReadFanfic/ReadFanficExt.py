from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem

from User.ReadFanfic.ReadFanfic import Ui_MainWindow
from libs.DataConnector import DataConnector
from libs.JsonFileFactory import JsonFileFactory


class ReadFanficExt(Ui_MainWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.json_factory = JsonFileFactory()
        self.fanfics = self.dc.get_all_fanfic()
        self.selected_index = -1

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
        self.show_fanfics_ui()
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        self.listWidget.setFont(font)
        self.lineEdit_Search.textChanged.connect(self.process_search)
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButton_Exit.clicked.connect(self.process_Exit)
        self.pushButton_Back.clicked.connect(self.go_back)
        self.pushButton_Search.clicked.connect(self.process_search)
        self.listWidget.itemSelectionChanged.connect(self.process_show_fanfic_detail)
        self.show_fanfics_ui()

    def show_fanfics_ui(self):
        self.listWidget.clear()
        for fanfic in self.fanfics:
            item = QListWidgetItem(fanfic.FanficTitle)
            item.setData(256, fanfic)
            self.listWidget.addItem(item)

    def process_show_fanfic_detail(self):
        index=self.listWidget.currentRow()
        if index<0:
            return
        self.selected_index=index
        fanfic=self.fanfics[index]
        self.lineEdit_Title.setText(fanfic.FanficTitle)
        self.lineEdit_Author.setText(fanfic.FanficAuthor)
        self.lineEdit_Date.setText(fanfic.FanficDateReleased)
        self.lineEdit_Character.setText(fanfic.FanficCharacters)
        self.textEdit.setText(fanfic.FanficContent)

    def process_search(self):
        search_text = self.lineEdit_Search.text().strip().lower()
        if not search_text:
            self.show_fanfics_ui()
            return

        filtered_fanfics = [fanfic for fanfic in self.fanfics if search_text in fanfic.FanficTitle.lower()]

        self.listWidget.clear()  # Xóa danh sách cũ
        for fanfic in filtered_fanfics:
            fanfic_item = QListWidgetItem(fanfic.FanficTitle)
            fanfic_item.setData(256, fanfic)
            self.listWidget.addItem(fanfic_item)

    def show_message(self, title, text, icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def process_Exit(self):
        msg = QMessageBox(self.MainWindow)
        msg.setWindowTitle("Confirm Exit!")
        msg.setText("Do you want to exit?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            exit()

    def go_back(self):
        self.MainWindow.close()  # Đóng cửa sổ hiện tại
        if self.previous_window:
            self.previous_window.show()  # Hiển thị lại cửa sổ trước đó

