from libs.JsonFileFactory import JsonFileFactory
from models.Draft import Draft
from models.Fanfic import Fanfic
from models.Film import Film
from models.Manager import Manager
from models.User import User
from models.browseFanfic import browseFanfic


class DataConnector:
    def __init__(self):
        self.current_user = None
    def get_all_fanfic(self):
        jff = JsonFileFactory()
        filename = "../dataset/fanfic.json"
        Ffic=jff.read_data(filename,Fanfic)
        return Ffic

    def get_all_user(self):
        jff = JsonFileFactory()
        filename = "../dataset/users.json"
        user= jff.read_data(filename,User)
        return user

    def get_all_manager(self):
        jff = JsonFileFactory()
        filename = "../dataset/managers.json"
        manager = jff.read_data(filename,Manager )
        return manager

    def get_all_film(self):
        jff = JsonFileFactory()
        filename = "../dataset/film.json"
        flm = jff.read_data(filename, Film)
        return flm

    def get_all_draft(self):
        jff = JsonFileFactory()
        filename = "../dataset/draft.json"
        draft = jff.read_data(filename, Draft)  # Đọc dữ liệu thay vì ghi
        return draft

    def get_all_browse_fanfic(self):
        jff = JsonFileFactory()
        filename = "../dataset/browse_fanfic.json"
        Ffic=jff.read_data(filename, browseFanfic)
        return Ffic

    def get_user_fanfic(self):
        users = self.get_all_user()

        # Giả sử ở đây bạn đang lấy user đăng nhập đầu tiên (có thể sau này thay đổi logic nếu cần)
        if not users:
            return []
        author = self.current_user.UserName

        jff = JsonFileFactory()
        result = []
        filename = f"../dataset/draft.json"
        draft_list = jff.read_data(filename, Draft)
        if draft_list:
            # Lọc ra tất cả draft của author
            author_drafts = [draft for draft in draft_list if draft.FanficAuthor == author]
            result.extend(author_drafts)



        return result

    def login_user(self, UserLoginName, Password):
        users = self.get_all_user()
        for user in users:
            if user.UserLoginName == UserLoginName and user.Password == Password:
                self.current_user = user  # lưu user hiện tại
                return True
        return None

    def login_manager(self, ManagerLoginName, Password):
        managers = self.get_all_manager()
        for m in managers:
            if m.ManagerLoginName == ManagerLoginName and m.Password == Password:
                return True
        return None

    def check_existing_user(self, users, userid):
        for i in range(len(users)):
            user = users[i]
            if user.UserID == userid:
                return i
        return -1

    def check_user_draft(self, users, author):
        for i in range(len(users)):
            user = users[i]
            if user.UserName == author:
                return i
        return -1
