import os
import sys
import json
import certifi
from dotenv import load_dotenv
import pandas as pd
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        def csv_to_json(self, file_path):
            try:
                data = pd.read_csv(file_path)
                data.reset_index(drop=True, inplace=True)

                records = list(json.loads(data.T.to_json()).values())

                return records
            except Exception as e:
                raise NetworkSecurityException(e, sys)
        
        def insert_data_to_mongodb(self, records, datbase, collection):
            try:
                self.records = records
                self.database = datbase
                self.collection = collection

                self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            except Exception as e:
                raise NetworkSecurityException(e, sys)