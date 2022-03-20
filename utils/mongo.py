from ast import List
import os
from pydoc import doc
from typing import Collection
import pymongo

class Mongo:
    
    __client: any
    __database: any
    __collection: any
    
    def __init__(self):
        self.__client = pymongo.MongoClient(
            host=os.environ['DATABASE_HOST'],
            port=int(os.environ['DATABASE_PORT']),
            username=os.environ['DATABASE_USERNAME'],
            password=os.environ['DATABASE_PASSWORD'],
        )
        self.__database = self.__client[os.environ['PRIMARY_DATABASE']]
        
        
    def insert_one(self, value):
        self.__collection = self.__database[os.environ['PRIMARY_COLLECTION']]
        self.__collection.insert_one(value)
        
    def insert_many(self, value):
        self.__collection = self.__database[os.environ['PRIMARY_COLLECTION']]
        self.__collection.insert_many(value)

    def update_one(self, query, value):
        self.__collection = self.__database[os.environ['PRIMARY_COLLECTION']]
        self.__collection.update_one(query, value)

    def get_documents_count(self):
        self.__collection = self.__database[os.environ['PRIMARY_COLLECTION']]
        return self.__collection.count_documents({})
    
    def get_all_documents(self):
        self.__collection = self.__database[os.environ['PRIMARY_COLLECTION']]
        documents = []
        for document in self.__collection.find({}):
          documents.append(document)
        return documents