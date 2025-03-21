import json
import os

from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem

from Manager.Browser.BrowserFanfic import Ui_MainWindow
from libs.DataConnector import DataConnector
from models.Fanfic import Fanfic


class BrowserFanficExt(Ui_MainWindow):
    def __init__(self, previous_window=None,user_management_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.fanfics = self.dc.get_all_browse_fanfic()
        self.selected_fanfic = None
        self.approved_titles = set()
        self.user_management_window = user_management_window

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.show_fanfic_ui()
        self.load_approved_titles()
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
        self.listWidget.itemSelectionChanged.connect(self.xem_chi_tiet)
        self.pushButton_Search.clicked.connect(self.process_search)
        self.pushButton_Remove.clicked.connect(self.process_remove)
        self.pushButton_Approved.clicked.connect(self.process_approve)

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

    def show_fanfic_ui(self):
        self.listWidget.clear()
        for fanfic in self.fanfics:
            fanfic_item = QListWidgetItem(fanfic.FanficTitle)
            fanfic_item.setData(256, fanfic)
            self.listWidget.addItem(fanfic_item)
            if fanfic.FanficTitle in self.approved_titles:
                fanfic_item.setBackground(QBrush(QColor(166, 209, 80)))


    def xem_chi_tiet(self):
        """Hiển thị thông tin chi tiết phim khi chọn trong listWidget."""
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            return
        selected_fanfic = selected_items[0].data(256)
        if selected_fanfic:
            self.lineEdit_Title.setText(selected_fanfic.FanficTitle)
            self.lineEdit_Date.setText(selected_fanfic.FanficDateReleased)
            self.lineEdit_Author.setText(str(selected_fanfic.FanficAuthor))
            self.lineEdit_Character.setText(selected_fanfic.FanficCharacters)
            self.textEdit.setText(selected_fanfic.FanficContent)
            self.selected_fanfic = selected_fanfic

    def process_search(self):
        search_text = self.lineEdit_Search.text().strip().lower()
        self.listWidget.clear()

        if not search_text:
            self.show_fanfic_ui()
            return

        for fanfic in self.fanfics:
            if search_text in fanfic.FanficTitle.lower():
                fanfic_item = QListWidgetItem(fanfic.DTitle)
                fanfic_item.setData(256, fanfic)
                self.listWidget.addItem(fanfic_item)
                if fanfic.FanficTitle in self.approved_titles:
                    fanfic_item.setBackground(QBrush(QColor(166, 209, 80)))

        if self.listWidget.count() == 0:
            no_result_item = QListWidgetItem("Không tìm thấy kết quả phù hợp")
            no_result_item.setForeground(QBrush(QColor(255, 0, 0)))
            self.listWidget.addItem(no_result_item)


    def process_remove(self):
        """Xóa vĩnh viễn fanfic được chọn khỏi danh sách và cập nhật lại dữ liệu"""
        if not self.selected_fanfic:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Chưa chọn fanfic để xóa!")
            return

        confirm = QMessageBox.question(
            self.MainWindow, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa fanfic: {self.selected_fanfic.FanficTitle}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            # Xóa fanfic khỏi danh sách dữ liệu
            self.fanfics = [fanfic for fanfic in self.fanfics if fanfic.FanficTitle != self.selected_fanfic.FanficTitle]

            # Xóa khỏi listWidget
            selected_row = self.listWidget.currentRow()
            if selected_row >= 0:
                self.listWidget.takeItem(selected_row)

            # Xóa nội dung trên giao diện
            self.lineEdit_Title.clear()
            self.lineEdit_Date.clear()
            self.lineEdit_Author.clear()
            self.lineEdit_Character.clear()
            self.textEdit.clear()

            # Ghi lại dữ liệu sau khi xóa
            self.save_to_database()

            QMessageBox.information(self.MainWindow, "Thành công", "Fanfic đã được xóa vĩnh viễn!")
            self.selected_fanfic = None

    def save_to_database(self):
        """Lưu danh sách fanfic vào file JSON trong thư mục ../dataset/"""
        dataset_path = "../dataset/browse_fanfic.json"

        # Đảm bảo thư mục dataset tồn tại
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

        # Ghi dữ liệu vào file JSON
        with open(dataset_path, "w", encoding="utf-8") as file:
            json.dump([fanfic.__dict__ for fanfic in self.fanfics], file, indent=4, ensure_ascii=False)

        print(f"Dữ liệu đã được lưu vào {dataset_path}")

    def process_approve(self):
       try:
           selected_items = self.listWidget.selectedItems()
           if not selected_items:
               QMessageBox.warning(self.MainWindow, "Lỗi", "Chưa chọn fanfic để duyệt!")
               return

           selected_item = selected_items[0]
           selected_fanfic = selected_item.data(256)

           if selected_fanfic.FanficTitle in self.approved_titles:
               QMessageBox.warning(self.MainWindow, "Lỗi", "Fanfic này đã được duyệt trước đó!")
               return

           self.approved_titles.add(selected_fanfic.FanficTitle)
           selected_item.setBackground(QBrush(QColor(166, 209, 80)))
           self.listWidget.clearSelection()  # Bỏ chọn tiêu đề ngay sau khi tô màu
           self.listWidget.repaint()  # Cập nhật giao diện ngay lập tức

           approved_path = "../dataset/approved_fanfic.json"
           fanfic_path = "../dataset/fanfic.json"
           os.makedirs(os.path.dirname(approved_path), exist_ok=True)

           approved_fanfics = []
           if os.path.exists(approved_path):
               try:
                   with open(approved_path, "r", encoding="utf-8") as file:
                       data = file.read().strip()
                       if data:
                           approved_fanfics = json.loads(data)
                       else:
                           approved_fanfics = []
               except json.JSONDecodeError:
                   approved_fanfics = []

           approved_fanfics.append(selected_fanfic.__dict__)
           with open(approved_path, "w", encoding="utf-8") as file:
               json.dump(approved_fanfics, file, indent=4, ensure_ascii=False)

           fanfics = []
           if os.path.exists(fanfic_path):
               try:
                   with open(fanfic_path, "r", encoding="utf-8") as file:
                       data = file.read().strip()
                       if data:
                           fanfics = json.loads(data)
                       else:
                           fanfics = []
               except json.JSONDecodeError:
                   fanfics = []

           fanfics.append(selected_fanfic.__dict__)
           with open(fanfic_path, "w", encoding="utf-8") as file:
               json.dump(fanfics, file, indent=4, ensure_ascii=False)

           self.update_fanfic_number(selected_fanfic.FanficAuthor)
           QMessageBox.information(self.MainWindow, "Thành công", f"Fanfic '{selected_item.text()}' đã được duyệt!")
           if self.user_management_window:
               self.user_management_window.refresh_users_table()


       except Exception as e:
           print(f"Error in approve: {e}")

    def update_fanfic_number(self, author):
        users_path = "../dataset/users.json"
        with open(users_path, "r", encoding="utf-8") as file:
            users = json.load(file)

        for user in users:
            if user["UserName"] == author:
                user["FanficNumber"] = str(int(user["FanficNumber"]) + 1)
                break

        with open(users_path, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

    def load_approved_titles(self):
        approved_path = "../dataset/approved_fanfic.json"
        self.approved_titles.clear()

        approved_titles = []

        if os.path.exists(approved_path):
            try:
                with open(approved_path, "r", encoding="utf-8") as file:
                    data = file.read().strip()
                    if data:
                        approved_fanfics = json.loads(data)
                        approved_titles = [fanfic.get("FanficTitle", "") for fanfic in approved_fanfics]
                        self.approved_titles = {fanfic.get("FanficTitle", "") for fanfic in approved_fanfics}
                    else:
                        approved_fanfics = []
            except (json.JSONDecodeError, FileNotFoundError):
                print("Lỗi khi đọc JSON từ approved_fanfic.json. Có thể tệp rỗng hoặc không hợp lệ.")
                approved_fanfics = []

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            if item.text() in approved_titles:
                item.setBackground(QBrush(QColor(166, 209, 80)))

    def load_from_database(self):
        dataset_path = "../../dataset/browse_fanfic.json"
        if os.path.exists(dataset_path):
            with open(dataset_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.fanfics = [Fanfic(
                    fanfic_dict["FanficTitle"],
                    fanfic_dict["FanficCharacters"],
                    fanfic_dict["FanficDateReleased"],
                    fanfic_dict["FanficAuthor"],
                    fanfic_dict["FanficContent"]
                ) for fanfic_dict in data]
            self.listWidget.clear()
            for fanfic in self.fanfics:
                self.listWidget.addItem(fanfic.FanficTitle)