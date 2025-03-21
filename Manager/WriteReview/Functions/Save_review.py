import json
import os
from datetime import datetime

from PyQt6.QtWidgets import QMessageBox, QListWidgetItem

from models.Film import Film


def save_review(self):
    """Lưu bài review vào save_reviewnew.json nếu nhập đủ thông tin"""

    # Lấy dữ liệu từ giao diện
    film_title = self.lineEdit_Title.text().strip()
    # Tự động cập nhật thời gian hiện tại
    film_date = datetime.now().strftime("%d-%m-%Y")  # Định dạng ngày-tháng-năm
    self.lineEdit_Date.setText(film_date)  # Hiển thị trên giao diện
    #film_date = self.lineEdit_Date.text().strip()
    film_author = self.lineEdit_Author.text().strip()
    film_characters = self.lineEdit_Character.text().strip()
    film_link = self.lineEdit_LinkFilm.text().strip()
    film_content = self.textEdit.toPlainText().strip()
    film_poster=getattr(self.selected_film,'PosterPath','')
    # Kiểm tra các trường bắt buộc
    if not film_title or not film_content:
        QMessageBox.warning(self.MainWindow, "Error", "Please enter Title and Content before saving!")
        return  # Không lưu nếu thiếu dữ liệu

    # Đảm bảo thư mục tồn tại
    directory = "../dataset"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, "save_reviewnew.json")

    # Đọc dữ liệu cũ từ file JSON
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    # Chuyển danh sách dict trong JSON thành danh sách `Film` object
    existing_reviews = [Film(**review) for review in data]

    # Tạo đối tượng Film mới
    new_film = Film(
        FilmTitle=film_title,
        FilmCharacters=film_characters,
        FilmDateReleased=film_date,
        FilmAuthor=film_author,
        LinkFilm=film_link,
        Content=film_content,
        PosterPath=film_poster
    )


    # check bài  bị lặp
    for review in existing_reviews:
        if review.FilmTitle.lower() == film_title.lower():
            QMessageBox.warning(self.MainWindow, "Error", "This review has been saved before!")
            return  # Dừng lại, không lưu nếu trùng lặp
    # Thêm bài review mới vào danh sách
    existing_reviews.append(new_film)
    # Chuyển danh sách `Film` object thành danh sách dict để lưu vào JSON
    updated_data = [film.__dict__ for film in existing_reviews]

    # Ghi lại file JSON
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(updated_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error in saving file: {e}")
        QMessageBox.warning(self.MainWindow, "Lỗi", f"Can not save file: {e}")
        return

    #Hiển thị bài viết mới lên listWidget dưới dạng Film object**
    film_item = QListWidgetItem(new_film.FilmTitle)  # Hiển thị tên phim
    film_item.setData(256, new_film)  # Lưu đối tượng Film vào item
    self.listWidget.addItem(film_item)  # Thêm vào listWidget

    QMessageBox.information(self.MainWindow, "Successfully", "Your review has already saved and be showed on list!")