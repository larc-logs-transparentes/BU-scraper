import os
import requests
import pymongo

BACKEND_URL = 'http://127.0.0.1:9090'


def commit_all_trees():
    response = requests.post(f'{BACKEND_URL}/tree/commit-all-trees')
    print(response.json())
    return response


def send_file_to_backend(file_path: str):
    print(f"Sending file {file_path} to backend")
    with open(file_path, "rb") as file:
        response = requests.post(f'{BACKEND_URL}/bu/create', files={"file": (os.path.basename(file_path), file)})
        print(response.json())
    
        return response


def read_bu_or_busa_files():
    files = [os.path.join(root, name)
                for root, dirs, files in os.walk("./assets/bus")
                for name in files if name.endswith(("-bu.dat", "-busa.dat"))]
    
    if not files:
        files = os.listdir("./assets/mocked_bus")
        files = [f"./assets/mocked_bus/{file}" for file in files]

    return files

# envia BUs na ordem em que foram recebidos pelo servidor do TSE
def read_bu_or_busa_files_in_order():
    nome_colecao = "primeiro_turno"

    client = pymongo.MongoClient("mongodb://localhost:8090/")
    db = client["bu"]
    collection = db[nome_colecao]
    collection.create_index([("timestamp", pymongo.ASCENDING)])

    cursor = collection.find({}, {"path": 1, "_id": 0}).sort("timestamp", 1)

    files = ["./" + doc["path"] for doc in cursor]

    return files

def insert_list_bus_to_db():
    for file in read_bu_or_busa_files_in_order():
        send_file_to_backend(file)
    print("---- Finished")

if __name__ == '__main__':
    insert_list_bus_to_db()
    commit_all_trees()
