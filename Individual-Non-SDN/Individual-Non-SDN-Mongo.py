import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://ayush:ayush@cluster0.pgkqn44.mongodb.net/Sanctions-List-Search?retryWrites=true&w=majority")
db = client["Sanctions-List-Search"]
collection = db["Individual-Non-SDN"]

with open('Individual-Non-SDN.json', 'r') as file:
    data = json.load(file)

collection.insert_many(data)
print("Data inserted successfully.")