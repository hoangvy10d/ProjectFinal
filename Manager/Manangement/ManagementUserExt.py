from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from matplotlib import pyplot as plt

from Manager.Browser.BrowserFanficExt import BrowserFanficExt
from Manager.Manangement.ManagementUser import Ui_MainWindow
from Manager.WriteReview.WriteReviewExt import WriteReviewExt
from libs.DataConnector import DataConnector
from libs.JsonFileFactory import JsonFileFactory
from models.User import User


class ManagementUserExt(Ui_MainWindow):
    def __init__(self, previous_window=None,manager_name=""):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.users = self.dc.get_all_user()  ##hiển thị toàn bộ users giả lập trên json file
        self.showing_vip = False
        self.showing_search = False
        self.manager_name = manager_name
        self.vip_users = []



    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.show_users_ui()
        self.setupSignalAndSlot()
        self.label_2.setText(self.manager_name)
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButton_Browser.clicked.connect(self.process_Browser)
        self.pushButton_WriteReview.clicked.connect(self.process_WriteReview)
        self.pushButton_Back.clicked.connect(self.go_back)
        self.tableWidget.itemSelectionChanged.connect(self.process_show_USER_detail)
        self.pushButton_Chart.clicked.connect(self.show_fanfic_bar_graph)
        self.pushButton_Delete.clicked.connect(self.delete_user)
        self.pushButton_Filter_Vip.clicked.connect(self.process_vip)
        self.pushButton_UpgradeVIP.clicked.connect(self.upgrade_vip)
        self.pushButton_Clear.clicked.connect(self.clear_detail_data)
        self.pushButton_Search.clicked.connect(self.process_search)
        self.pushButton_Exit.clicked.connect(self.process_Exit)

    def process_Exit(self):
        msg = QMessageBox(self.MainWindow)
        msg.setWindowTitle("Confirm Exit!")
        msg.setText("Do you want to exit?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            exit()

    def process_Browser(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = BrowserFanficExt(self.MainWindow, user_management_window=self)
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()

    def process_WriteReview(self):
        self.MainWindow.close()  # close login window
        self.mainwindow = QMainWindow()
        self.myui = WriteReviewExt(self.MainWindow)
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()

    def go_back(self):
        self.MainWindow.close()  # Đóng cửa sổ hiện tại
        if self.previous_window:
            self.previous_window.show()  # Hiển thị lại cửa sổ trước đó

    def refresh_users_table(self):
        self.users = self.dc.get_all_user()  # Lấy dữ liệu mới từ file JSON
        self.show_users_ui()

    def show_users_ui(self):
        # remove existing data from QTable Widget
        self.tableWidget.setRowCount(0)
        current_users = self.vip_users if self.showing_vip else self.users
        # add product item into QTableWidget:
        for p in current_users:
            # return number of row (meaning: last row)
            row = self.tableWidget.rowCount()
            # insert a new row:
            self.tableWidget.insertRow(row)
            # create columns:
            col_UserID = QTableWidgetItem(p.UserID)
            col_UserName = QTableWidgetItem(p.UserName)
            col_UserLoginName = QTableWidgetItem(str(p.UserLoginName))
            col_Password = QTableWidgetItem(str(p.Password))
            col_Email = QTableWidgetItem(str(p.Email))
            col_SignUpDate = QTableWidgetItem(str(p.SignUpDate))
            col_FanficNumber = QTableWidgetItem(str(p.FanficNumber))
            # set cell for row:
            self.tableWidget.setItem(row, 0, col_UserID)
            self.tableWidget.setItem(row, 1, col_UserName)
            self.tableWidget.setItem(row, 2, col_UserLoginName)  # thêm cái này vô table
            self.tableWidget.setItem(row, 3, col_Password)
            self.tableWidget.setItem(row, 4, col_Email)
            self.tableWidget.setItem(row, 5, col_SignUpDate)
            self.tableWidget.setItem(row, 6, col_FanficNumber)
            if self.showing_vip:
                col_UserID.setBackground(QColor(255, 0, 0))
                col_UserName.setBackground(QColor(255, 0, 0))
                col_UserLoginName.setBackground(QColor(255, 0, 0))
                col_Password.setBackground(QColor(255, 0, 0))
                col_Email.setBackground(QColor(255, 0, 0))
                col_SignUpDate.setBackground(QColor(255, 0, 0))
                col_FanficNumber.setBackground(QColor(255, 0, 0))

    def process_show_USER_detail(self):
        index = self.tableWidget.currentRow()
        if index < 0:
            return
        if self.showing_vip:
            current_users = [user for user in self.users if int(user.FanficNumber) >= 10]
        elif hasattr(self, 'search_results') and self.search_results:
            current_users = self.search_results
        else:
            current_users = self.users

            # Đảm bảo index hợp lệ
        if index >= len(current_users):
            return

        user = current_users[index]
        print(f"Selected user: {user.UserID}, FanficNumber: {user.FanficNumber}")  # Debug
        self.lineEdit_UserId.setText(user.UserID)
        self.lineEdit_UserName.setText(user.UserName)
        self.lineEdit_UserLoginName.setText(user.UserLoginName)  # thêm cái này vô chỗ detail user
        self.lineEdit_Password.setText(str(user.Password))
        self.lineEdit_Email.setText(str(user.Email))
        self.lineEdit_SignUpDate.setText(str(user.SignUpDate))
        self.lineEdit_FanficNumber.setText(str(user.FanficNumber))

    def clear_detail_data(self):
        self.lineEdit_UserId.clear()
        self.lineEdit_UserName.clear()
        self.lineEdit_UserLoginName.clear()
        self.lineEdit_Password.clear()
        self.lineEdit_Email.clear()
        self.lineEdit_SignUpDate.clear()
        self.lineEdit_FanficNumber.clear()
        self.lineEdit_UserId.setFocus()

    def delete_user(self):
        #Step 1: Find the user that we want to remove
        UserID=self.lineEdit_UserId.text()
        self.users=self.dc.get_all_user()
        index=self.dc.check_existing_user(self.users,UserID)
        if index==-1:#not found->then end the algorithm
            return
        #Step 2: Remove user by index
        self.users.pop(index)
        #Step 3: Save all data into Hard Disk:
        jff = JsonFileFactory()
        filename = "../dataset/users.json"
        jff.write_data(self.users, filename)
        # Step 4: Re-display data into GUI:
        self.users =self.dc.get_all_user()
        self.show_users_ui() #cap nhat bang khach hang
        self.clear_detail_data()

    def process_vip(self):
        try:
            print("Button VIP clicked!")
            print(f"Users: {self.users}")

            self.tableWidget.setRowCount(0)
            # add product item into QTableWidget:
            if not self.showing_vip:  # Hiện tại đang hiển thị tất cả -> chuyển sang chỉ VIP
                print("Switching to VIP list")
                self.vip_users = [p for p in self.users if int(p.FanficNumber) >= 10]
                print(f"VIP Users filtered: {self.vip_users}")
                for p in self.vip_users:
                    print(f"Processing Users: {p.UserID}")
                    try:
                        fanfic_num = int(p.FanficNumber)  # Ép kiểu để so sánh
                        if fanfic_num >= 10:  # Chỉ hiển thị user VIP
                            row = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(row)
                            col_UserID = QTableWidgetItem(p.UserID)
                            col_UserName = QTableWidgetItem(p.UserName)
                            col_UserLoginName = QTableWidgetItem(str(p.UserLoginName))
                            col_Password = QTableWidgetItem(str(p.Password))
                            col_Email = QTableWidgetItem(str(p.Email))
                            col_SignUpDate = QTableWidgetItem(str(p.SignUpDate))
                            col_FanficNumber = QTableWidgetItem(str(p.FanficNumber))
                            self.tableWidget.setItem(row, 0, col_UserID)
                            self.tableWidget.setItem(row, 1, col_UserName)
                            self.tableWidget.setItem(row, 2, col_UserLoginName)
                            self.tableWidget.setItem(row, 3, col_Password)
                            self.tableWidget.setItem(row, 4, col_Email)
                            self.tableWidget.setItem(row, 5, col_SignUpDate)
                            self.tableWidget.setItem(row, 6, col_FanficNumber)
                            # Tô màu đỏ cho user VIP
                            print(f"Adding VIP user {p.UserID} with FanficNumber {fanfic_num}")
                            col_UserID.setBackground(QColor(255, 0, 0))
                            col_UserName.setBackground(QColor(255, 0, 0))
                            col_UserLoginName.setBackground(QColor(255, 0, 0))
                            col_Password.setBackground(QColor(255, 0, 0))
                            col_Email.setBackground(QColor(255, 0, 0))
                            col_SignUpDate.setBackground(QColor(255, 0, 0))
                            col_FanficNumber.setBackground(QColor(255, 0, 0))
                        self.showing_vip = True
                    except ValueError:
                        print(f"Cannot convert FanficNumber {p.FanficNumber} to int - skipping")
            else:  # Hiện tại đang hiển thị VIP -> chuyển về tất cả
                print("Switching back to full list")
                self.showing_vip = False
                self.show_users_ui()

                for p in self.users:
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    col_UserID = QTableWidgetItem(p.UserID)
                    col_UserName = QTableWidgetItem(p.UserName)
                    col_UserLoginName = QTableWidgetItem(str(p.UserLoginName))
                    col_Password = QTableWidgetItem(str(p.Password))
                    col_Email = QTableWidgetItem(str(p.Email))
                    col_SignUpDate = QTableWidgetItem(str(p.SignUpDate))
                    col_FanficNumber = QTableWidgetItem(str(p.FanficNumber))
                    self.tableWidget.setItem(row, 0, col_UserID)
                    self.tableWidget.setItem(row, 1, col_UserName)
                    self.tableWidget.setItem(row, 2, col_UserLoginName)
                    self.tableWidget.setItem(row, 3, col_Password)
                    self.tableWidget.setItem(row, 4, col_Email)
                    self.tableWidget.setItem(row, 5, col_SignUpDate)
                    self.tableWidget.setItem(row, 6, col_FanficNumber)
                    # Không tô màu khi hiển thị toàn bộ
                # Chuyển trạng thái về tất cả

            print("Process VIP completed successfully!")
        except Exception as e:
            print(f"Error in process_vip: {e}")

    def upgrade_vip(self):
        try:
            print("Button Upgrade VIP clicked!")

            # Lọc danh sách VIP từ self.users (giữ nguyên đối tượng User)
            new_vip_users = [p for p in self.users if int(p.FanficNumber) >= 10]
            print(f"New VIP Users to append: {new_vip_users}")

            if not new_vip_users:
                print("No new VIP users found!")
                return

            # Đường dẫn tệp VIP
            vip_filename = "../dataset/vip_users.json"

            # Đọc dữ liệu hiện có từ vip_users.json (nếu tồn tại)
            existing_vip_users = []
            try:
                with open(vip_filename, 'r', encoding='utf-8') as file:
                    import json
                    data = json.load(file)
                    # Chuyển dữ liệu JSON thành danh sách đối tượng User
                    existing_vip_users = [User(**item) for item in data]
                    print(f"Existing VIP Users loaded: {existing_vip_users}")
            except FileNotFoundError:
                print(f"{vip_filename} not found, creating new file.")
            except Exception as e:
                print(f"Error loading existing VIP users: {e}")

            # Tạo một tập hợp các UserID hiện có để kiểm tra trùng lặp nhanh chóng
            existing_user_ids = {user.UserID for user in existing_vip_users}

            # Chỉ thêm những user mới không trùng UserID
            unique_new_vip_users = []
            for new_user in new_vip_users:
                if new_user.UserID not in existing_user_ids:
                    unique_new_vip_users.append(new_user)
                    existing_user_ids.add(new_user.UserID)  # Cập nhật tập hợp UserID

            # Nếu không có user mới nào sau khi lọc trùng, thoát
            if not unique_new_vip_users:
                print("No unique new VIP users to add!")
                return

            # Thêm các user mới không trùng vào danh sách hiện có
            existing_vip_users.extend(unique_new_vip_users)
            print(f"Updated VIP Users after removing duplicates: {existing_vip_users}")

            # Ghi danh sách đã cập nhật vào tệp
            jff = JsonFileFactory()
            jff.write_data(existing_vip_users, vip_filename)
            print(
                f"Appended {len(unique_new_vip_users)} unique VIP users to {vip_filename}. Total: {len(existing_vip_users)}")

            print("Upgrade VIP completed successfully!")
        except Exception as e:
            print(f"Error in upgrade_vip: {e}")

    def show_fanfic_bar_graph(self):
        try:
            # Lấy danh sách FanficNumber từ tất cả người dùng
            fanfic_numbers = [int(user.FanficNumber) for user in self.users if user.FanficNumber]

            if not fanfic_numbers:
                print("No valid FanficNumber data found!")
                return

            # Xác định các khoảng (bins) cho FanficNumber
            bins = [0, 5, 10, 15, 20, float('inf')]  # Các khoảng: 0-5, 6-10, 11-15, 16-20, >20
            labels = ['0-5', '6-10', '11-15', '16-20', '>20']  # Nhãn cho từng khoảng

            # Đếm số người dùng trong mỗi khoảng
            counts = [0] * (len(bins) - 1)
            for num in fanfic_numbers:
                for i in range(len(bins) - 1):
                    if bins[i] <= num < bins[i + 1]:
                        counts[i] += 1
                        break

            # Tạo biểu đồ dạng thanh
            plt.figure(figsize=(10, 6))
            plt.bar(labels, counts, color='lightcoral')
            plt.xlabel('Number of Fanfic')
            plt.ylabel('Number of User')
            plt.title('Distribution of the Number of Fanfics by Users')
            plt.tight_layout()
            # Hiển thị biểu đồ
            plt.show()
        except Exception as e:
            print(f"Error in show_fanfic_bar_graph: {e}")

    def process_search(self):
        """Tìm kiếm user theo tên và hiển thị kết quả trong Table"""
        search_text = self.lineEdit_SearchID.text().strip().lower()  # Lấy ID nhập vào

        if not search_text:  # Nếu ô tìm kiếm trống, hiển thị lại toàn bộ danh sách
            self.show_users_ui()
            return

        filtered_users = [user for user in self.users if search_text in user.UserID.lower()]  # Lọc user

        self.tableWidget.setRowCount(0)  # Xóa dữ liệu cũ
        self.search_results = filtered_users  # Lưu kết quả tìm kiếm

        for user in filtered_users:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(user.UserID))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(user.UserName))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(user.UserLoginName))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(user.Password))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(user.Email))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(user.SignUpDate))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(str(user.FanficNumber)))






