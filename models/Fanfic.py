class Fanfic:
    def __init__(self, FanficTitle, FanficCharacters, FanficDateReleased, FanficAuthor, FanficContent):
        self.FanficTitle = FanficTitle
        self.FanficCharacters = FanficCharacters
        self.FanficDateReleased = FanficDateReleased
        self.FanficAuthor = FanficAuthor
        self.FanficContent = FanficContent

    def __str__(self):
        return f"{self.FanficTitle}\t{self.FanficCharacters}\t{self.FanficDateReleased}\t{self.FanficAuthor}\t{self.FanficContent}"



