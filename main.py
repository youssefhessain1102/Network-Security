import sys
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    try:
        trainig_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=trainig_pipeline_config)
        data_ingstion = DataIngestion(data_ingestion_config)
        logging.info('Initiate Data ingestion')
        data_ingestion_artifacts = data_ingstion.initiate_data_ingestion()
        print(data_ingestion_artifacts)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
