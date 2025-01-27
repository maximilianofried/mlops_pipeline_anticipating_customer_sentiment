import logging
import mlflow
import pandas as pd
from zenml import step
from typing_extensions import Annotated
from typing import Tuple
from sklearn.base import RegressorMixin
from model.evaluation import MSE, RMSE, R2
from zenml.client import Client

experiment_tracker = Client().active_stack.experiment_tracker

@step(experiment_tracker=experiment_tracker.name)
def evaluate_model(
    model: RegressorMixin,
    X_test: pd.DataFrame,
    y_test: pd.DataFrame,
    ) -> Tuple[
        Annotated[float, "r2_Score"],
        Annotated[float, "rmse"],
    ]:
    """
    Evaluates the model on the ingested data

    Args:
        model: RegressorMixin,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
    """
    try:
        prediction = model.predict(X_test)

        mse_class = MSE()
        mse = mse_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("mse", mse)
        r2_class = R2()
        r2 = r2_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("r2", r2)
        rmse_class = RMSE()
        rmse = rmse_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("rmse", rmse)
        return r2, rmse
    except Exception as e:
        logging.error(f"Error evaluating model: {e}")
        raise e