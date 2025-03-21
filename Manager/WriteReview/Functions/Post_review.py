from datetime import datetime

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox

from libs.JsonFileFactory import JsonFileFactory
from models.Film import Film


def post_review(self):
    try:
        if self.selected_film != -1:
            # Hiển thị hộp thoại xác nhận
            confirm_dialog = QMessageBox()
            confirm_dialog.setIcon(QMessageBox.Icon.NoIcon)
            confirm_dialog.setWindowTitle("Confirm Post")
            confirm_dialog.setText("Are you sure you want to post this script?")
            confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = confirm_dialog.exec()
            if result == QMessageBox.StandardButton.Yes:
                # Lấy dữ liệu từ các trường input
                FilmTitle = self.lineEdit_Title.text().strip()
                #tự động cập nhật time hiện tại
                FilmDateReleased=datetime.now().strftime("%d-%m-%Y")
                self.lineEdit_Date.setText(FilmDateReleased)
                #FilmDateReleased = self.lineEdit_Date.text().strip()
                FilmAuthor = self.lineEdit_Author.text().strip()
                FilmCharacters = self.lineEdit_Character.text().strip()
                LinkFilm = self.lineEdit_LinkFilm.text().strip()
                Content = self.textEdit.toPlainText().strip()
                # Lấy đường dẫn poster
                if self.selected_film != -1 and hasattr(self.selected_film, 'PosterPath'):
                    film_poster = self.selected_film.PosterPath  # Dùng PosterPath từ selected_film nếu có
                else:
                    film_poster = ""  # Mặc định là rỗng nếu chưa có poster
                # Kiểm tra trùng lặp dựa trên FilmTitle
                for existing_film in self.films:
                    if existing_film.FilmTitle.lower() == FilmTitle.lower():
                        QMessageBox.warning(
                            self.MainWindow if hasattr(self, 'MainWindow') else None,
                            "Duplicate Error",
                            "A review with this title already exists!"
                        )
                        return  # Thoát khỏi hàm nếu phát hiện trùng lặp
                # Tạo đối tượng Film
                new_film = Film(
                    FilmTitle=FilmTitle,
                    FilmCharacters=FilmCharacters,
                    FilmDateReleased=FilmDateReleased,
                    FilmAuthor=FilmAuthor,
                    LinkFilm=LinkFilm,
                    Content=Content,
                    PosterPath=film_poster
                )

                # Thêm vào danh sách films
                self.films.append(new_film)

                # Ghi dữ liệu vào file JSON
                jff = JsonFileFactory()
                filename = "../dataset/film.json"
                jff.write_data(self.films, filename)

                # Tìm bài vừa post trong listWidget và tô màu ngay
                for index in range(self.listWidget.count()):
                    item = self.listWidget.item(index)
                    if item.text() == FilmTitle:
                        item.setBackground(QColor(144, 238, 144))  # Tô màu xanh lá nhạt
                        break  # Dừng vòng lặp ngay khi tìm thấy

                self.listWidget.update()  # Cập nhật giao diện

                # Hiển thị thông báo thành công
                QMessageBox.information(self.MainWindow if hasattr(self, 'MainWindow') else None,
                                       "Success", "Upload bài thành công!")


        else:
            QMessageBox.warning(self.MainWindow if hasattr(self, 'MainWindow') else None,
                               "Error", "Please pick a script!")
    except Exception as e:
        # Bắt lỗi tổng quát nếu có vấn đề trước khi hiển thị thông báo
        QMessageBox.critical(None, "Critical Error", f"Failed to post review: {str(e)}")