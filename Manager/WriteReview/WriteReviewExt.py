import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QFileDialog
from PyQt6.uic.properties import QtWidgets

from Manager.WriteReview.Functions.Post_review import post_review
from Manager.WriteReview.Functions.Save_review import save_review
from Manager.WriteReview.WriteReview import Ui_MainWindow
from libs.DataConnector import DataConnector
from models.Film import Film


class WriteReviewExt(Ui_MainWindow):
    SAVE_FILE = "../dataset/save_reviewnew.json"
    POST_FILE = "../dataset/film.json"
    POSTER = "D:/Users/LENOVO/baicuaThao/ProjectFinal/Poster"
    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.dc = DataConnector()
        self.films = self.dc.get_all_film()
        self.selected_film = -1
        # Lưu trữ posted_titles từ film.json một lần duy nhất
        self.posted_titles = self._load_posted_titles()


    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        font = QFont()
        font.setPointSize(13)
        self.listWidget.setFont(font)
        self.textEdit.setFont(font)
        self.load_reviewnew()
        self.lineEdit_Search.textChanged.connect(self.process_search)

    def showWindow(self):
        self.MainWindow.show()

    def _load_posted_titles(self):
        """Tải danh sách tiêu đề đã đăng từ film.json một lần"""
        posted_titles = set()
        if os.path.exists(self.POST_FILE):
            try:
                with open(self.POST_FILE, "r", encoding="utf-8") as file:
                    posted_reviews = json.load(file)
                    if isinstance(posted_reviews, list):
                        posted_titles = {review.get("FilmTitle", "") for review in posted_reviews}
                    else:
                        posted_titles = set()
            except json.JSONDecodeError:
                QMessageBox.critical(self.MainWindow, "Error", "File film.json bị hỏng.")
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi đọc file film.json: {e}")
        return posted_titles

    def _is_posted(self, review_data):
        """Kiểm tra xem review có trong danh sách đã đăng không"""
        return review_data["FilmTitle"] in self.posted_titles

    def _load_reviews_from_file(self, file_path):
        """Đọc và trả về danh sách review từ file JSON"""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    reviews = json.load(file)
                    if isinstance(reviews, list):
                        return [
                            Film(
                                FilmTitle=r.get("title", r.get("FilmTitle", "")),
                                FilmCharacters=r.get("characters", r.get("FilmCharacters", "")),
                                FilmDateReleased=r.get("date_released", r.get("FilmDateReleased", "")),
                                FilmAuthor=r.get("author", r.get("FilmAuthor", "")),
                                LinkFilm=r.get("link_film", r.get("LinkFilm", "")),
                                Content=r.get("content", r.get("Content", "")),
                                PosterPath=r.get("posterpath", r.get("PosterPath", ""))
                            ) for r in reviews
                        ]
                    return []
            except json.JSONDecodeError:
                QMessageBox.critical(self.MainWindow, "Error", f"File {file_path} bị hỏng.")
                return []
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi đọc file {file_path}: {e}")
                return []
        return []

    def load_reviewnew(self):
        """Hiển thị toàn bộ review từ save_reviewnew.json"""
        self.listWidget.clear()
        saved_films = self._load_reviews_from_file(self.SAVE_FILE)
        for film in saved_films:
            film_item = QListWidgetItem(film.FilmTitle)
            film_item.setData(256, film)
            if self._is_posted({
                "FilmTitle": film.FilmTitle,
                "FilmCharacters": film.FilmCharacters,
                "FilmDateReleased": film.FilmDateReleased,
                "FilmAuthor": film.FilmAuthor,
                "LinkFilm": film.LinkFilm,
                "Content": film.Content,
                "PosterPath": film.PosterPath
            }):
                film_item.setBackground(QColor(144, 238, 144))
            self.listWidget.addItem(film_item)
        self.listWidget.update()
    def setupSignalAndSlot(self):
        self.pushButton_Exit.clicked.connect(self.process_Exit)
        self.pushButton_Back.clicked.connect(self.go_back)
        self.listWidget.itemSelectionChanged.connect(self.xem_chi_tiet)
        self.pushButton_Search.clicked.connect(self.process_search)
        self.pushButton_Save.clicked.connect(lambda: save_review(self))
        self.pushButton_Post.clicked.connect(lambda: post_review(self))
        self.pushButton_Clear.clicked.connect(self.process_Clear)
        self.pushButton_SelectImage.clicked.connect(self.processImages)


    def process_Clear(self):
        self.lineEdit_Author.setText("")
        self.lineEdit_Character.setText("")
        self.lineEdit_LinkFilm.setText("")
        self.textEdit.setText("")
        self.lineEdit_Title.setText("")
        self.lineEdit_Title.setFocus()
        self.lineEdit_Date.setText("")
        self.label_Image.clear()

    def processImages(self):
        """Mở thư mục Poster, chọn ảnh và hiển thị lên labelPoster"""
        try:
            poster_path, _ = QFileDialog.getOpenFileName(
                self.MainWindow,
                "Chọn Poster Film",
                self.POSTER,
                "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )

            if poster_path:
                pixmap = QPixmap(poster_path)
                if pixmap.isNull():
                    QMessageBox.warning(self.MainWindow, "Lỗi", "Không thể tải ảnh được chọn.")
                    return

                scaled_pixmap = pixmap.scaled(
                    self.label_Image.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label_Image.setPixmap(scaled_pixmap)
                self.label_Image.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Lưu đường dẫn tương đối
                relative_path = os.path.relpath(poster_path, self.POSTER)
                if self.selected_film == -1:  # Nếu chưa có film được chọn (tạo mới)
                    self.selected_film = Film(
                        FilmTitle=self.lineEdit_Title.text().strip(),
                        FilmCharacters=self.lineEdit_Character.text().strip(),
                        FilmDateReleased=self.lineEdit_Date.text().strip(),
                        FilmAuthor=self.lineEdit_Author.text().strip(),
                        LinkFilm=self.lineEdit_LinkFilm.text().strip(),
                        Content=self.textEdit.toPlainText().strip(),
                        PosterPath=relative_path
                    )
                else:  # Cập nhật film hiện tại
                    self.selected_film.PosterPath = relative_path
                print(f"Updated PosterPath in processImages: {self.selected_film.PosterPath}")  # Debug

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Lỗi khi xử lý ảnh: {e}")

    def xem_chi_tiet(self):
        """Hiển thị thông tin chi tiết phim khi chọn trong listWidget"""
        try:
            selected_items = self.listWidget.selectedItems()
            if not selected_items:
                return
            selected_film = selected_items[0].data(256)
            if isinstance(selected_film, dict):
                selected_film = Film(**selected_film)
            if selected_film:
                self.lineEdit_Title.setText(selected_film.FilmTitle)
                self.lineEdit_Date.setText(selected_film.FilmDateReleased)
                self.lineEdit_Author.setText(str(selected_film.FilmAuthor))
                self.lineEdit_Character.setText(selected_film.FilmCharacters)
                self.lineEdit_LinkFilm.setText(selected_film.LinkFilm)
                self.textEdit.setText(selected_film.Content)
                self.selected_film = selected_film
                # Hiển thị poster
                if selected_film.PosterPath:
                    poster_path = os.path.join(self.POSTER, selected_film.PosterPath)
                    if os.path.exists(poster_path):
                        pixmap = QPixmap(poster_path)
                        scaled_pixmap = pixmap.scaled(
                            self.label_Image.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        self.label_Image.setPixmap(scaled_pixmap)
                        self.label_Image.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    else:
                        self.label_Image.clear()
                        QMessageBox.warning(self.MainWindow, "Warning", f"Không tìm thấy poster: {poster_path}")
                else:
                    self.label_Image.clear()
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi hiển thị chi tiết: {e}")

    def process_search(self):
        """Tìm kiếm phim trong save_reviewnew.json"""
        try:
            search_text = self.lineEdit_Search.text().strip().lower()
            if not search_text:
                self.load_reviewnew()
                return
            self.listWidget.clear()
            saved_films = self._load_reviews_from_file(self.SAVE_FILE)
            filtered_films = [film for film in saved_films if search_text in film.FilmTitle.lower()]
            for film in filtered_films:
                film_item = QListWidgetItem(film.FilmTitle)
                film_item.setData(256, film)
                if self._is_posted({
                    "FilmTitle": film.FilmTitle,
                    "FilmCharacters": film.FilmCharacters,
                    "FilmDateReleased": film.FilmDateReleased,
                    "FilmAuthor": film.FilmAuthor,
                    "LinkFilm": film.LinkFilm,
                    "Content": film.Content
                }):
                    film_item.setBackground(QColor(144, 238, 144))
                self.listWidget.addItem(film_item)
            self.listWidget.update()
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi tìm kiếm: {e}")

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