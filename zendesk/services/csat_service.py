from zendesk.mongo.mongo_client import MongoClientInterface

class CSATService:
    def __init__(self):
        self.mongo_client = MongoClientInterface()

    def save_data(self, request):
        return self.mongo_client.save_document(request.data)

    def test(self):
        return self.mongo_client.test()
