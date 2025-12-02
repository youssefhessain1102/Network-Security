import numpy as np
import pandas as pd
import sys
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constant.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARMAS,
    TARGET_COLUMN,
)
from network_security.logging.logger import logging
from network_security.config.artifacts_entity import (
    DataValidationArtifact,
    DataTransformationArtifact,
)
from network_security.config.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import save_object, save_numpy_array_data


class DataTransformation:
    def __init__(
        self,
        data_validation_artifacts: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifacts: DataValidationArtifact = (
                data_validation_artifacts
            )
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def data_transformer_object(cls):
        logging.info("Started Getting data transformer object")

        try:
            knn_imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARMAS)
            preprocessor: Pipeline = Pipeline([("knn_imputer", knn_imputer)])
            return preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Started Data Transformation")
            train_data = self.read_data(
                self.data_validation_artifacts.valid_train_file_path
            )
            test_data = self.read_data(
                self.data_validation_artifacts.valid_test_file_path
            )

            X_train = train_data.drop(columns=[TARGET_COLUMN])
            y_train = train_data[TARGET_COLUMN].replace(-1, 0)

            X_test = test_data.drop(columns=[TARGET_COLUMN])
            y_test = test_data[TARGET_COLUMN].replace(-1, 0)

            preprocessor = self.data_transformer_object()
            preprocessor_object = preprocessor.fit(X_train)
            X_train_transformed = preprocessor_object.transform(X_train)
            X_test_transformed = preprocessor_object.transform(X_test)

            train_arr = np.c_[X_train_transformed, np.array(y_train)]
            test_arr = np.c_[X_test_transformed, np.array(y_test)]

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, train_arr
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, test_arr
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            save_object('final_model/preprocessor.pkl', preprocessor_object)


            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)
