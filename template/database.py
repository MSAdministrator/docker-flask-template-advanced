from pymongo import DESCENDING, MongoClient, ASCENDING
from template.config import Config


class Database:

    def __init__(self):
        self.uri = f"mongodb://{Config.MONGODB_USERNAME}:{Config.MONGODB_PASSWORD}@{Config.MONGODB_HOST}:{Config.MONGODB_PORT}"
        self.client = MongoClient(self.uri)
        self.database = self.client[Config.MONGODB_DB]
        self.database.domains.create_index(
            [('value', ASCENDING)],
            unique=True
        )
        self.database.ips.create_index(
            [('value', ASCENDING)],
            unique=True
        )


database_session = Database()
