import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.uic.properties import QtWidgets

from User.ReadReview.ReadReview import Ui_MainWindow
from libs.DataConnector import DataConnector


class ReadReviewExt(Ui_MainWindow):
    POSTER = "D:/Users/LENOVO/baicuaThao/ProjectFina/Poster"
    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.film = self.dc.get_all_film()
        self.selected_film = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
        self.show_film_ui()
        font = QFont()
        font.setPointSize(13)
        self.textEdit.setFont(font)
        self.lineEdit_Search.textChanged.connect(self.process_search)


    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButton_Exit.clicked.connect(self.process_Exit)
        self.pushButton_Back.clicked.connect(self.go_back)
        self.listWidget.itemSelectionChanged.connect(self.xem_chi_tiet)
        self.pushButton_Search.clicked.connect(self.process_search)  # Gán sự kiện cho nút Search
        self.show_film_ui()

    def show_film_ui(self):
        """Hiển thị danh sách phim trong listWidgetRead."""
        self.listWidget.clear()  # Xóa danh sách cũ

        for film in self.film:
            film_item = QListWidgetItem(film.FilmTitle)  # Hiển thị tiêu đề phim
            film_item.setData(256, film)  # Lưu đối tượng film vào item
            self.listWidget.addItem(film_item)

    def xem_chi_tiet(self):
        """Hiển thị thông tin chi tiết phim khi chọn trong listWidget."""
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            return
        selected_film = selected_items[0].data(256)  # Lấy đối tượng film từ item
        if selected_film:
            self.lineEdit_Title.setText(selected_film.FilmTitle)
            self.lineEdit_Date.setText(selected_film.FilmDateReleased)
            self.lineEdit_Author.setText(str(selected_film.FilmAuthor))
            self.lineEditCharacters.setText(selected_film.FilmCharacters)
            self.lineEdit_LinkFilm.setText(selected_film.LinkFilm)
            self.textEdit.setText(selected_film.Content)  ####đổi thành
            self.selected_film = selected_film
            # Hiển thị poster
            if selected_film.PosterPath:
                poster_path = os.path.join(self.POSTER, selected_film.PosterPath)
                if os.path.exists(poster_path):
                    pixmap = QPixmap(poster_path)
                    # Điều chỉnh kích thước ảnh để phù hợp với labelPoster
                    scaled_pixmap = pixmap.scaled(
                        self.label_poster.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.label_poster.setPixmap(scaled_pixmap)
                    self.label_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)

                else:
                    self.label_poster.clear()
                    QMessageBox.warning(self.MainWindow, "Warning", f"Không tìm thấy poster: {poster_path}")
            else:
                self.label_poster.clear()


    def process_search(self):
        """Tìm kiếm phim theo tên và hiển thị kết quả trong listWidget"""
        search_text = self.lineEdit_Search.text().strip().lower()  # Lấy tên phim nhập vào

        if not search_text:  # Nếu ô tìm kiếm trống, hiển thị lại toàn bộ danh sách
            self.show_film_ui()
            return

        filtered_films = [film for film in self.film if search_text in film.FilmTitle.lower()]  # Lọc phim

        self.listWidget.clear()  # Xóa danh sách cũ
        for film in filtered_films:
            film_item = QListWidgetItem(film.FilmTitle)  # Hiển thị tên phim
            film_item.setData(256, film)  # Lưu đối tượng phim vào item
            self.listWidget.addItem(film_item)

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
