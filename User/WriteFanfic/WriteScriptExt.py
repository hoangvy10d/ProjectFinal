
from datetime import datetime

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem

from User.WriteFanfic.WriteScript import Ui_MainWindow
from libs.DataConnector import DataConnector
from libs.JsonFileFactory import JsonFileFactory
from models.Draft import Draft


class WriteScriptExt(Ui_MainWindow):
    def __init__(self, previous_window=None, data_connector=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = data_connector or  DataConnector()
        self.json_factory = JsonFileFactory()
        self.fanfics = self.dc.get_all_fanfic()
        self.browsefanfics = self.dc.get_all_browse_fanfic()
        self.drafts = self.dc.get_user_fanfic()
        self.selected_draft = None
        self.selected_index = -1
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
        self.show_drafts_ui()
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        self.listWidget.setFont(font)
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButton_Exit.clicked.connect(self.process_Exit)
        self.pushButton_Back.clicked.connect(self.go_back)
        self.pushButton_Post.clicked.connect(self.process_post)
        self.pushButton_Search.clicked.connect(self.process_search)
        self.pushButton_Save.clicked.connect(self.process_save)
        self.pushButton_Update.clicked.connect(self.process_update)
        self.listWidget.itemSelectionChanged.connect(lambda: self.process_show_draft_detail())

    def show_drafts_ui(self):
        self.listWidget.clear()

        for draft in self.drafts:
            item = QListWidgetItem(draft.FanficTitle)
            for fanfic in self.fanfics:
                if fanfic.FanficTitle == draft.FanficTitle and fanfic.FanficContent == draft.FanficContent:
                    item.setBackground(QColor("yellow"))
            self.listWidget.addItem(item)

    def process_show_draft_detail(self):
        index = self.listWidget.currentRow()
        print(f"Selected index: {index}")  # Debug: Kiểm tra index lấy từ listWidget

        if not self.drafts:
            self.show_message("Error", "No drafts available!", QMessageBox.Icon.Warning)
            return

        if index < 0 or index >= len(self.drafts):  # Kiểm tra index có hợp lệ không
            self.show_message("Error", f"Invalid draft selection! (index: {index})", QMessageBox.Icon.Warning)
            return

        # Cập nhật chỉ số đang chọn
        self.selected_index = index
        draft = self.drafts[index]  # Lấy draft từ danh sách
        print(f"Selected draft: {draft.FanficTitle}")  # Debug: Kiểm tra draft lấy ra

        # Hiển thị dữ liệu lên giao diện
        self.lineEdit_Title.setText(draft.FanficTitle)
        self.lineEdit_Author.setText(draft.FanficAuthor)
        self.lineEdit_Date.setText(draft.FanficDateReleased)
        self.lineEdit_Character.setText(draft.FanficCharacters)
        self.textEdit.setText(draft.FanficContent)

    def process_update(self):
        if self.selected_index == -1:
            self.show_message("Error", "Please select a draft to update!", QMessageBox.Icon.Warning)
            return

        # Lấy thông tin mới từ UI
        title = self.lineEdit_Title.text().strip()
        author = self.lineEdit_Author.text().strip()
        characters = self.lineEdit_Character.text().strip()
        content = self.textEdit.toPlainText().strip()
        current_time = datetime.now().strftime("%d-%m-%Y")

        if not content:
            self.show_message("Notice", "There is no script to update.", QMessageBox.Icon.Warning)
            return

        try:
            jff = JsonFileFactory()
            main_filename = "../dataset/draft.json"

            # Đọc toàn bộ dữ liệu từ file JSON để không bị ghi đè
            all_drafts = jff.read_data(main_filename, Draft)

            # Kiểm tra vị trí tương ứng trong danh sách
            if 0 <= self.selected_index < len(self.drafts):
                draft = self.drafts[self.selected_index]

                # Cập nhật nội dung của draft trong danh sách
                for i, d in enumerate(all_drafts):
                    if d.FanficTitle == draft.FanficTitle and d.FanficContent == draft.FanficContent:
                        all_drafts[i].FanficTitle = title
                        all_drafts[i].FanficAuthor = author
                        all_drafts[i].FanficCharacters = characters
                        all_drafts[i].FanficContent = content
                        all_drafts[i].FanficDateReleased = current_time
                        break

                # Ghi lại danh sách vào file JSON
                jff.write_data(all_drafts, main_filename)

                # ✅ Cập nhật lại danh sách trên giao diện
                self.show_drafts_ui()

                # Giữ nguyên trạng thái chọn
                self.listWidget.setCurrentRow(self.selected_index)

                self.show_message("Notice", "Draft updated successfully!", QMessageBox.Icon.Information)
            else:
                self.show_message("Error", "Invalid draft index!", QMessageBox.Icon.Warning)

        except Exception as e:
            self.show_message("Error", f"Failed to update draft: {str(e)}", QMessageBox.Icon.Critical)
    def process_post(self):
        if self.selected_index == -1:
            # Nếu chưa chọn script thì báo lỗi ngay
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Please pick a script!")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return  # Dừng luôn

        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Icon.Question)
        confirm_dialog.setWindowTitle("Confirm Post")
        confirm_dialog.setText("Are you sure you want to post this script?")
        confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = confirm_dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            title = self.lineEdit_Title.text().strip()
            author = self.lineEdit_Author.text().strip()
            characters = self.lineEdit_Character.text().strip()
            post_content = self.textEdit.toPlainText().strip()
            current_time = datetime.now().strftime("%d-%m-%Y")
            self.lineEdit_Date.setText(current_time)

            for fanfic in self.fanfics:
                if fanfic.FanficTitle == title and fanfic.FanficContent == post_content:
                    self.show_message("Notice", "You have already posted this script!", QMessageBox.Icon.Information)
                    return

            bf = Draft(title, characters, current_time, author, post_content)
            self.browsefanfics.append(bf)
            filename = "../dataset/browse_fanfic.json"
            self.json_factory.write_data(self.browsefanfics, filename)

            self.show_message("Notice", "Posted successfully! Your post is now being verified.",
                              QMessageBox.Icon.Information)



    # Phương thức save draft mới
    def process_save(self):
        title = self.lineEdit_Title.text().strip()
        author = self.lineEdit_Author.text().strip()
        characters = self.lineEdit_Character.text().strip()
        post_content = self.textEdit.toPlainText().strip()
        current_time = datetime.now().strftime("%d-%m-%Y")
        self.lineEdit_Date.setText(current_time)

        if not post_content:
            self.show_message("Notice", "There is no script to save.", QMessageBox.Icon.Warning)
            return

        # Tạo đối tượng Draft mới
        new_draft = Draft(title, characters, current_time, author, post_content)

        try:
            jff = JsonFileFactory()
            main_filename = "../dataset/draft.json"

            # 1️⃣ Đọc dữ liệu cũ
            old_drafts = jff.read_data(main_filename, Draft)
            if not old_drafts:
                old_drafts = []

            # 2️⃣ Thêm draft mới vào danh sách
            old_drafts.append(new_draft)

            # 3️⃣ Ghi lại danh sách vào file
            jff.write_data(old_drafts, main_filename)

            # 4️⃣ ✅ Cập nhật danh sách `listWidget`

            self.listWidget.addItem(title)

            self.show_message("Notice", "Saved successfully", QMessageBox.Icon.Information)

        except Exception as e:
            self.show_message("Error", f"Failed to save draft: {str(e)}", QMessageBox.Icon.Critical)
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
            self.previous_window.show()

    def process_search(self):
        search_text = self.lineEdit_Search.text().strip().lower()  # Lấy tên phim nhập vào

        if not search_text:  # Nếu ô tìm kiếm trống, hiển thị lại toàn bộ danh sách
            self.show_drafts_ui()
            return

        filtered_drafts = [draft for draft in self.drafts if search_text in draft.FanficTitle.lower()]  # Lọc phim

        self.listWidget.clear()  # Xóa danh sách cũ
        for draft in filtered_drafts:
            draft_item = QListWidgetItem(draft.FanficTitle)  # Hiển thị tên phim
            draft_item.setData(256, draft)  # Lưu đối tượng phim vào item
            self.listWidget.addItem(draft_item)

