import os
import sys
from network_security.config.artifacts_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network_security.config.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import (
    evaluate_models,
    save_object,
    load_object,
    load_numpy_array_data,
)
from network_security.utils.model_utils.metric_utils import get_classification_score
from network_security.utils.model_utils.model_utils import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
    GradientBoostingClassifier,
)
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifacts: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        try:
            self.data_transformation_artifacts: DataTransformationArtifact = (
                data_transformation_artifacts
            )
            self.model_trainer_config: ModelTrainerConfig = model_trainer_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "LogisticRegression": LogisticRegression(),
            "DecisionTreeClassifier": DecisionTreeClassifier(),
            "RandomForestClassifier": RandomForestClassifier(verbose=1),
            "KNeighborsClassifier": KNeighborsClassifier(),
            "AdaBoostClassifier": AdaBoostClassifier(),
            "GradientBoostingClassifier": GradientBoostingClassifier(),
            "XGBClassifier": XGBClassifier(),
        }

        params = {
            "DecisionTreeClassifier": {
                "criterion": ["gini", "entropy", "log_loss"],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "RandomForestClassifier": {
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                "n_estimators": [8, 16, 32, 128, 256]
            },
            "GradientBoostingClassifier": {},
            "LogisticRegression": {},
            "AdaBoostClassifier": {
                "learning_rate": [0.1, 0.01, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "XGBClassifier": {},
            "KNeighborsClassifier": {"n_neighbors": [3, 4, 5, 7, 9]},
        }

        model_report: dict = evaluate_models(
            X_train, y_train, X_test, y_test, models, params
        )

        best_model_score = max(sorted(model_report.values()))

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        trained_model = get_classification_score(y_train, y_train_pred)
        testing_model = get_classification_score(y_test, y_test_pred)

        preprocessor = load_object(
            self.data_transformation_artifacts.transformed_object_file_path
        )

        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor, best_model)

        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            object=network_model,
        )

        model_trainer_artifact = ModelTrainerArtifact(
            self.model_trainer_config.trained_model_file_path,
            trained_metric_artifact=trained_model,
            tested_metric_artifact=testing_model,
        )

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_path = self.data_transformation_artifacts.transformed_train_file_path
            test_path = self.data_transformation_artifacts.transformed_test_file_path

            train_arr = load_numpy_array_data(train_path)
            test_arr = load_numpy_array_data(test_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact: ModelTrainerArtifact = self.train_model(
                X_train, y_train, X_test, y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
