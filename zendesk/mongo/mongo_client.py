import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

class MongoClientInterface:
    def __init__(self):
        self.uri = f"mongodb+srv://{os.environ.get('MONGODB_USER')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOST')}/?retryWrites=true&w=majority"
        # self.uri = "mongodb+srv://joseferreira:f2UMT3hzlqro4np8@csat.in72g.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri)

    def test(self):
        try:
            print(self.client.server_info())  # Isso forçará a conexão e mostrará info do servidor
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def connect(self):
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return self.client
        except Exception as e:
            print(e)

    def save_document(self, document):
        conn = self.connect()
        database = conn[os.environ.get("MONGODB_DATABASE")]
        collection = database[os.environ.get("MONGODB_COLLECTION")]
        response = collection.insert_one(document)
        conn.close()

        return response
