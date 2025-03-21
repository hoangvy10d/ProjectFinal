from libs.JsonFileFactory import JsonFileFactory
from models.Film import Film

jff=JsonFileFactory()
filename="../dataset/films.json"
films=jff.read_data(filename,Film)
print("list of films from json:")
for p in films:
    print(p)