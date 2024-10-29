import os
import json
from azure.cosmos import CosmosClient, PartitionKey

# Load endpoint and key from local.settings.json
config_path = (
    'C:/WORKSPACE/Serverless-API/chelseafc_api/local.settings.json'
)
try:
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Configuration file not found: {config_path}")
    exit(1)


# Initialize Cosmos DB client
endpoint = os.getenv('COSMOS_DB_ENDPOINT')  # or replace with your endpoint
key = os.getenv('COSMOS_DB_KEY')  # or replace with your key
client = CosmosClient(endpoint, key)

# Create database and container if they don't exist
database_name = 'ChelseaFCDB'
container_name = 'PlayersCollection'

database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

# Sample data for Chelsea FC players
players = [
    {
        "id": "1",
        "name": "Marc Cucurella Saseta",
        "position": "Left-back, left wing-back",
        "number": 3,
        "Place of birth": "Alella, Spain",
        "dob": "07-22-1998",
        "coverUrl": "url-to-image-in-cloud-storage"
    },

    {
        "id": "2",
        "name": "Moises Isaac Caicedo Corozo",
        "position": "Defensive midfielder",
        "number": 25,
        "Place of birth": "Santo Domingo, Ecuador",
        "dob": "11-02-2001",
        "coverUrl": "url-to-image-in-cloud-storage"
    },

    {
        "id": "3",
        "name": "Cole Jermaine Palmer",
        "position": "Attacking midfielder, winger",
        "number": 20,
        "Place of birth": "Manchester, England",
        "dob": "05-06-2002",
        "coverUrl": "url-to-image-in-cloud-storage"
    }
    # Add more players here

]

# Insert players into Cosmos DB
for player in players:
    container.create_item(body=player)

print("Player data successfully uploaded to Cosmos DB!")
