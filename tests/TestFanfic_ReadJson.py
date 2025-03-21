from libs.JsonFileFactory import JsonFileFactory
from models.Fanfic import Fanfic

jff=JsonFileFactory()
filename="../dataset/fanfic.json"
fanfics=jff.read_data(filename,Fanfic)
print("List of Fanfics:")
for f in fanfics:
    print(f)