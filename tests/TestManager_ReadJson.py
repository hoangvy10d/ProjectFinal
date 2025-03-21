from libs.JsonFileFactory import JsonFileFactory
from models.Manager import Manager

jff=JsonFileFactory()
filename="../dataset/managers.json"
managers=jff.read_data(filename,Manager)
print("Danh sách caác quản lí:")
for m in managers:
    print(m)