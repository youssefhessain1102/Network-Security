from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
import sys
from network_security.components.model_trainer import ModelTrainer
from network_security.config.config_entity import (
    DataIngestionConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.config.artifacts_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact,
)


class TrainingPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingstion = DataIngestion(data_ingestion_config)
            logging.info("Initiate Data ingestion")

            data_ingestion_artifacts = data_ingstion.initiate_data_ingestion()
            logging.info("Ingestion Initiation completed")

            return data_ingestion_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(
        self, data_ingestion_artifacts: DataIngestionArtifact
    ) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(
                data_ingestion_artifacts, data_validation_config
            )
            logging.info("Initiate Data Validation")

            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info("Validation Initiation completed")

            return data_validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(
        self, data_validation_artifacts: DataValidation
    ) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(
                self.training_pipeline_config
            )
            data_transformation = DataTransformation(
                data_validation_artifacts, data_transformation_config
            )
            logging.info("Initiate Data Transformation")

            data_transformation_artifacts = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Transformation Initiation completed")

            return data_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_training(
        self, data_transformation_artifacts: DataTransformation
    ) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(
                data_transformation_artifacts, model_trainer_config
            )
            logging.info("Initiate Model Training")

            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Model Training Initiation completed")

            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_art = self.start_data_ingestion()
            data_validation_art = self.start_data_validation(data_ingestion_art)
            data_transformation_art = self.start_data_transformation(
                data_validation_art
            )
            model_trainer_art = self.start_model_training(data_transformation_art)

            return model_trainer_art
        except Exception as e:
            raise NetworkSecurityException(e, sys)
