class Manager:
    def __init__(self,ManagerID, ManagerName, ManagerLoginName, Password):
        self.ManagerID=ManagerID
        self.ManagerName=ManagerName
        self.ManagerLoginName=ManagerLoginName
        self.Password=Password
    def __str__(self):
        return f"{self.ManagerID}\t{self.ManagerName}\t{self.ManagerLoginName}\t{self.Password}"