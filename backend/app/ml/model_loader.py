import logging
import os
from dataclasses import dataclass

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from app.core.config import get_settings
from app.ml.classifier import LabelPrediction, TicketCategoryClassifier
from app.ml.priority import PriorityPredictor
from app.ml.sentiment import SentimentAnalyzer

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TicketAnalysis:
    category: LabelPrediction
    sentiment: LabelPrediction
    priority: LabelPrediction
    model_version: str


class SupportTicketAnalyzer:
    def __init__(self) -> None:
        # Baseline rule-based classifiers as fallback
        self.baseline_category = TicketCategoryClassifier()
        self.baseline_sentiment = SentimentAnalyzer()
        self.baseline_priority = PriorityPredictor()

        self.category_model = None
        self.sentiment_model = None
        self.priority_model = None

        self.model_version = get_settings().model_version

        # Initialize and load models
        self.load_models()

    def _get_latest_model_uri(self, model_name: str, tracking_uri: str) -> str:
        client = MlflowClient(tracking_uri=tracking_uri)
        # Fetch latest versions across all stages
        latest_versions = client.get_latest_versions(model_name, stages=["None", "Production", "Staging"])
        if latest_versions:
            # Sort by version string parsed as integer descending
            sorted_versions = sorted(latest_versions, key=lambda v: int(v.version), reverse=True)
            latest_version = sorted_versions[0].version
            return f"models:/{model_name}/{latest_version}"
        raise Exception(f"No registered versions found for model {model_name}")

    def load_models(self) -> None:
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
        mlflow.set_tracking_uri(tracking_uri)

        logger.info(f"Connecting to MLflow Tracking Server at {tracking_uri}...")

        try:
            logger.info("Resolving latest registered model versions from MLflow registry...")
            cat_uri = self._get_latest_model_uri("ticket_category_classifier", tracking_uri)
            sent_uri = self._get_latest_model_uri("ticket_sentiment_analyzer", tracking_uri)
            prio_uri = self._get_latest_model_uri("ticket_priority_predictor", tracking_uri)

            logger.info(f"Loading category model from URI: {cat_uri}")
            self.category_model = mlflow.sklearn.load_model(cat_uri)

            logger.info(f"Loading sentiment model from URI: {sent_uri}")
            self.sentiment_model = mlflow.sklearn.load_model(sent_uri)

            logger.info(f"Loading priority model from URI: {prio_uri}")
            self.priority_model = mlflow.sklearn.load_model(prio_uri)

            # Get the exact version numbers to display in model_version
            cat_version = cat_uri.split("/")[-1]
            self.model_version = f"mlflow-v{cat_version}"
            logger.info(f"Successfully loaded MLflow models (version {cat_version}).")
        except Exception as e:
            logger.warning(
                f"Failed to load models from MLflow registry: {e}. "
                f"Falling back to rule-based baseline classifiers."
            )
            self.category_model = None
            self.sentiment_model = None
            self.priority_model = None
            self.model_version = "baseline-v1"

    def analyze(self, subject: str, description: str) -> TicketAnalysis:
        text = f"{subject}\n{description}"

        # 1. Category Prediction
        if self.category_model is not None:
            try:
                probs = self.category_model.predict_proba([text])[0]
                classes = self.category_model.classes_
                max_idx = probs.argmax()
                cat_label = str(classes[max_idx])
                cat_conf = float(probs[max_idx])
                category = LabelPrediction(label=cat_label, confidence=cat_conf)
            except Exception as e:
                logger.error(f"Error predicting category using MLflow model: {e}")
                category = self.baseline_category.predict(text)
        else:
            category = self.baseline_category.predict(text)

        # 2. Sentiment Prediction
        if self.sentiment_model is not None:
            try:
                probs = self.sentiment_model.predict_proba([text])[0]
                classes = self.sentiment_model.classes_
                max_idx = probs.argmax()
                sent_label = str(classes[max_idx])
                sent_conf = float(probs[max_idx])
                sentiment = LabelPrediction(label=sent_label, confidence=sent_conf)
            except Exception as e:
                logger.error(f"Error predicting sentiment using MLflow model: {e}")
                sentiment = self.baseline_sentiment.predict(text)
        else:
            sentiment = self.baseline_sentiment.predict(text)

        # 3. Priority Prediction
        if self.priority_model is not None:
            try:
                probs = self.priority_model.predict_proba([text])[0]
                classes = self.priority_model.classes_
                max_idx = probs.argmax()
                prio_label = str(classes[max_idx])
                prio_conf = float(probs[max_idx])
                priority = LabelPrediction(label=prio_label, confidence=prio_conf)
            except Exception as e:
                logger.error(f"Error predicting priority using MLflow model: {e}")
                priority = self.baseline_priority.predict(text, sentiment.label)
        else:
            priority = self.baseline_priority.predict(text, sentiment.label)

        return TicketAnalysis(
            category=category,
            sentiment=sentiment,
            priority=priority,
            model_version=self.model_version,
        )


analyzer = SupportTicketAnalyzer()
