from models.Draft import Draft
from models.Fanfic import Fanfic


class browseFanfic(Fanfic):
    def __init__(self, FanficTitle, FanficCharacters, FanficDateReleased, FanficAuthor, FanficContent):
        super().__init__(FanficTitle, FanficCharacters, FanficDateReleased, FanficAuthor, FanficContent)
