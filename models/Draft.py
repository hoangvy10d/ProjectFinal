from models.Fanfic import Fanfic


class Draft(Fanfic):
    def __init__(self, FanficTitle, FanficCharacters, FanficDateReleased, FanficAuthor, FanficContent):
        super().__init__(FanficTitle, FanficCharacters, FanficDateReleased, FanficAuthor, FanficContent)
