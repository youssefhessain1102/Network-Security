# Common Constant variables for pipeline
TARGET_COLUMN: str = "result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACTS_DIR: str = "Artifacts"
DATA_SET_FILE: str = "network_data.csv"
TRAINING_FILE: str = 'train.csv'
TESTING_FILE: str = 'test.csv'
FILE_NAME: str = 'phisingData.csv'

# Data Ingestion Constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkDatabase"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2
