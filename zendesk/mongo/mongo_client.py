import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

class MongoClientInterface:
    def __init__(self):
        self.uri = f"mongodb+srv://{os.environ.get('MONGODB_USER')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOST')}/?retryWrites=true&w=majority"
        # self.client = MongoClient(self.uri)
        self.database = os.environ.get("MONGODB_DATABASE")
        self.collection = os.environ.get("MONGODB_COLLECTION")

    def get_client(self):
        """Garante que um novo cliente é criado sempre que necessário"""
        return MongoClient(self.uri)

    def test(self):
        """Testa se a conexão com o banco funciona"""
        try:
            client = self.get_client()
            print(client.server_info())  # Isso forçará a conexão e mostrará info do servidor
            client.close()
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def save_document(self, document):
        """Salva o documento no banco"""
        with self.get_client() as conn:
            database = conn[self.database]
            collection = database[self.collection]
            response = collection.insert_one(document)
            conn.close()

            return response
