import pymongo

class Database(object):
    URI = "mongodb+srv://Down:Miki55555115@discordbot.ar8mxva.mongodb.net/?retryWrites=true&w=majority"
    DATABASE = None
    
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["discord"]
    
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
        
    @staticmethod
    def insert_one(collection, data):
        Database.DATABASE[collection].insert_one(data)
        
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)
    
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
    
    @staticmethod
    def update_one(collection, query, update):
        Database.DATABASE[collection].update_one(query, update)
    
    @staticmethod
    def delete_one(collection, query):
        Database.DATABASE[collection].delete_one(query)
        
    @staticmethod
    def distinct(collection, query):
        return Database.DATABASE[collection].distinct(query)
    
    @staticmethod
    def list_documents(collection, field_names, include_id=True):
        filt = {name: 1 for name in field_names}
        filt["_id"] = 1 if include_id else 0
        return list(Database.DATABASE[collection].find({}, filt))