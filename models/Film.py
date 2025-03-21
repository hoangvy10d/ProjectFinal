import json


class Film:
    def __init__(self, FilmTitle, FilmCharacters, FilmDateReleased, FilmAuthor, LinkFilm,Content,PosterPath=""):
        self.FilmTitle = FilmTitle
        self.FilmCharacters = FilmCharacters
        self.FilmDateReleased = FilmDateReleased
        self.FilmAuthor = FilmAuthor
        self.LinkFilm = LinkFilm
        self.Content=Content
        self.PosterPath = PosterPath  # Thêm trường PosterPath
    def __str__(self):
        return f"{self.FilmTitle}\t{self.FilmCharacters}\t{self.FilmDateReleased}\t{self.FilmAuthor}\t{self.LinkFilm}\t{self.Content}"
def load_films_from_json(file_path):
    """Hàm đọc dữ liệu phim từ JSON và chuyển thành danh sách các đối tượng Film."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            films = [Film(**film_data) for film_data in data]  # Chuyển dữ liệu thành list Film
            return films
    except Exception as e:
        print(f"Lỗi khi đọc file JSON: {e}")
        return []