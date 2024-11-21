import json
import os


#Checar se a tabela e a coleção existe, se não criar.
def create_db_and_collections (client, db_name, collection_name):
    db = client[db_name]
    #List of collections in the database
    collections = db.list_collection_names()

#Check if collection exists if not, create it
    if collection_name not in collections:
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' create in database '{db_name}''")

    else:
        print(f"Collection '{collection_name}' already exists in database '{db_name}''")
    
    print("create collections Done")

    return collection_name 

def list_files_in_directories(dir):
    files = os.listdir(f"{dir}")
    
    return files

def files_into_mongodb(collection, db_name, file, client, dir ="."):
    """ 
        Insert the files into Mongo DB Collection
        
        Parameters:
        collection(str): Name of the collection that you want to insert data
        db_name(str): Database name
        file(str): File that you want to insert
        dir(str): Optional - Directory where the file is. Std value = "."
        client(str): Connection string to MongoDB server

        Returns:
        data: The data inserted into the collection
    """
    db = client[db_name]
    collection_db = db[collection]
    with open(f"{dir}/{file}", 'r') as f:
        print(f)
        data = json.load(f)
    # Check if data is a list (multiple documents) or a single document
    if isinstance(data, list):
        # Insert multiple documents
        collection_db.insert_many(data)
        print(f"Inserted {len(data)} documents into collection '{collection}' in database '{db_name}'.")
    else:
        # Insert a single document
        collection_db.insert_one(data)
        print(f"Inserted 1 document into collection '{collection}' in database '{db_name}'.")
    
    return data

def load_json_into_collection (collection_name, db_name, client, directory):
    print("Starting load...")
    try:
        files = list_files_in_directories(directory)  
        print(files)      
        for file in files:
            print(file)
            print(db_name)
            print(collection_name)
            print(client)
            print(directory)
            insert_data = files_into_mongodb(collection_name, db_name, file, client, directory)
            print(collection_name)

    except Exception as e:
        print(e)
    
    #return insert_data




