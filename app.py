import pymongo
from get_data import get_data_github
from load_data import *

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db_name = "PokemonDB"


from concurrent.futures import ThreadPoolExecutor

# def run_io_tasks_in_parallel(tasks):
#     with ThreadPoolExecutor() as executor:
#         running_tasks = [executor.submit(task) for task in tasks]
#         for running_task in running_tasks:
#             running_task.result()

# run_io_tasks_in_parallel([
#     lambda: print('IO task 1 running!'),
#     lambda: print('IO task 2 running!'),
# ])

if __name__ == "__main__":
    try:
        get1 = get_data_github("PokemonTCG/pokemon-tcg-data", "cards/en") #output: ('cards/en')
        get2 = get_data_github("PokemonTCG/pokemon-tcg-data", "decks/en")
        get3 = get_data_github("PokemonTCG/pokemon-tcg-data", "sets")
        create_coll1 = create_db_and_collections(client, db_name, 'CardsCollection') #output:collection name
        create_coll2 = create_db_and_collections(client, db_name, 'DecksCollection')
        create_coll3 = create_db_and_collections(client, db_name, 'SetsCollection')
        insert_files_mongodb1 = load_json_into_collection(create_coll1,db_name, client, get1)
        insert_files_mongodb2 = load_json_into_collection(create_coll2,db_name, client, get2)
        insert_files_mongodb3 = load_json_into_collection(create_coll3,db_name, client, get3)

    except Exception as e:
        print(e)


#use logging library - allow us to create level of logs