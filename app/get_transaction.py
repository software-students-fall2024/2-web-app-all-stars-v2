import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

database_url = os.getenv('DATABASE_ENDPOINT')

client = pymongo.MongoClient(database_url)

db = client["sample_supplies"]
collection = db["sales"]

def get_transaction(email):
    
    query = {"customer.email": email}
    transaction = collection.find_one(query)
    
    if transaction:
        return transaction
    else:
        return {"error": "Transaction not found"}