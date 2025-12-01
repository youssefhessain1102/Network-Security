import sys
from network_security.config.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

if __name__ == "__main__":
    try:

        # Data Ingestion
        trainig_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainig_pipeline_config)
        data_ingstion = DataIngestion(data_ingestion_config)
        logging.info("Initiate Data ingestion")

        data_ingestion_artifacts = data_ingstion.initiate_data_ingestion()
        logging.info("Ingestion Initiation completed")
        print(data_ingestion_artifacts)

        # Data Validation
        data_validation_config = DataValidationConfig(trainig_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifacts, data_validation_config
        )
        logging.info("Initiate Data Validation")

        data_validation_artifacts = data_validation.initiate_data_validation()
        logging.info("Validation Initiation completed")
        print(data_validation_artifacts)

        # Data Transformation
        data_transformation_config = DataTransformationConfig(trainig_pipeline_config)
        data_transformation = DataTransformation(
            data_validation_artifacts, data_transformation_config
        )
        logging.info("Initiate Data Transformation")

        data_transformation_artifacts = (
            data_transformation.initiate_data_transformation()
        )
        logging.info("Transformation Initiation completed")
        print(data_transformation_artifacts)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
