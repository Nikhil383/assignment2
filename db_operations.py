import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["data_query_db"]
collection = db["csv_data"]

def load_csv_to_mongodb(csv_file_path):
    try:
        collection.drop()
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            documents = [dict(row) for row in reader]
            for doc in documents:
                for key, value in doc.items():
                    if value.isdigit():
                        doc[key] = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        doc[key] = float(value)
            collection.insert_many(documents)
        print(f"Loaded {len(documents)} documents into MongoDB.")
    except Exception as e:
        print(f"Error loading CSV to MongoDB: {e}")
        raise

def execute_query(query):
    try:
        if query is None:
            return None
        results = list(collection.find(query))
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None