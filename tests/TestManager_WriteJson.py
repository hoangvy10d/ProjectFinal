from libs.JsonFileFactory import JsonFileFactory
from models.Manager import Manager

managers=[] #ManagerID, ManagerName, ManagerLoginName, Password
managers.append(Manager("K244111451","Hoàng Phương Anh","panh12345","12345"))
managers.append(Manager("K244111469","Trần Thị Nhật Minh","minhhihi","56807"))
managers.append(Manager("K244111478","Hồ Thị Phương Thảo","thaohoho","12345"))
managers.append(Manager("K244111486","Phạm Ngô Bảo Trân","tranngo135","trantran123"))
managers.append(Manager("K244111488","Nguyễn Hoàng Vy","vugoang123","vyvyvy6868"))
print("Danh sách Manager:")
for m in managers:
    print(m)
jff=JsonFileFactory()
filename="../dataset/managers.json"
jff.write_data(managers,filename)