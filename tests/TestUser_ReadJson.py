from libs.JsonFileFactory import JsonFileFactory
from models.User import User

jff=JsonFileFactory()
filename= "../dataset/users.json"
users=jff.read_data(filename,User)
print("Danh sách Manager:")
for u in users:
    print(u)