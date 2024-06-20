import logging
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

mongo_uri = "mongodb+srv://ayush:ayush@cluster0.pgkqn44.mongodb.net/Sanctions-List-Search?retryWrites=true&w=majority"
database_name = "Sanctions-List-Search"
aircraft_sdn_collection_name = "Aircraft-SDN"
entity_sdn_collection_name = "Entity-SDN"
individual_sdn_collection_name = "Individual-SDN"
vessel_sdn_collection_name = "Vessel-SDN"
entity_non_sdn_collection_name = "Entity-Non-SDN"
individual_non_sdn_collection_name = "Individual-Non-SDN"

def search_by_name(collection, Name):
    query = {
        "$or": [
            {"Name": {"$regex": f".*{Name}.*", "$options": "i"}},
            {"Aliases.Name": {"$regex": f".*{Name}.*", "$options": "i"}}
        ]
    }
    matching_records = collection.find(query)
    records_list = list(matching_records)
    return records_list

@app.route('/', methods=['GET', 'POST'])
def search_sanctions():
    if request.method == 'POST':
        Name = request.form.get('Name', '')
        logging.debug(f"Search Name: {Name}")
        if Name:
            client = MongoClient(mongo_uri)
            database = client[database_name]
            
            entity_sdn_collection = database[entity_sdn_collection_name]
            result_entity_sdn = search_by_name(entity_sdn_collection, Name)
            
            individual_non_sdn_collection = database[individual_non_sdn_collection_name]
            result_individual_non_sdn = search_by_name(individual_non_sdn_collection, Name)
            
            client.close()
            
            return render_template('index.html', result_entity_sdn=result_entity_sdn, result_individual_non_sdn=result_individual_non_sdn)
    return render_template('index.html')

@app.route('/individual_details/<int:id>')
def individual_details(id):
    try:
        client = MongoClient(mongo_uri)
        database = client[database_name]
        
        entity_sdn_collection = database[entity_sdn_collection_name]
        individual_non_sdn_collection = database[individual_non_sdn_collection_name]
        
        entity_sdn_record = entity_sdn_collection.find_one({"ID": id})
        individual_non_sdn_record = individual_non_sdn_collection.find_one({"ID": id})
        
        client.close()
        
        if entity_sdn_record:
            return render_template('individual_details.html', entity_sdn_record=entity_sdn_record)
        elif individual_non_sdn_record:
            return render_template('individual_details.html', individual_non_sdn_record=individual_non_sdn_record)
        else:
            return render_template('individual_details.html', id=id)
    except Exception as e:
        return str(e), 500

@app.route('/aircraft-sdn')
def display_aircraft_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    aircraft_sdn_collection = database[aircraft_sdn_collection_name]
    records = aircraft_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_table.html', records=records_list, title="Aircraft SDN")

@app.route('/entity-sdn')
def display_entity_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    entity_sdn_collection = database[entity_sdn_collection_name]
    records = entity_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_entity_sdn.html', records=records_list, title="Entity SDN")

@app.route('/individual-sdn')
def display_individual_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    individual_sdn_collection = database[individual_sdn_collection_name]
    records = individual_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_table.html', records=records_list, title="Individual SDN")

@app.route('/vessel-sdn')
def display_vessel_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    vessel_sdn_collection = database[vessel_sdn_collection_name]
    records = vessel_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_table.html', records=records_list, title="Vessel SDN")

@app.route('/entity-non-sdn')
def display_entity_non_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    entity_non_sdn_collection = database[entity_non_sdn_collection_name]
    records = entity_non_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_table.html', records=records_list, title="Entity Non-SDN")

@app.route('/individual-non-sdn')
def display_individual_non_sdn():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    individual_non_sdn_collection = database[individual_non_sdn_collection_name]
    records = individual_non_sdn_collection.find()
    records_list = list(records)
    client.close()
    return render_template('display_individual_non_sdn.html', records=records_list, title="Individual Non-SDN")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
