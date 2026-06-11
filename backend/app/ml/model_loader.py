from dataclasses import dataclass

from app.core.config import get_settings
from app.ml.classifier import LabelPrediction, TicketCategoryClassifier
from app.ml.priority import PriorityPredictor
from app.ml.sentiment import SentimentAnalyzer


@dataclass(frozen=True)
class TicketAnalysis:
    category: LabelPrediction
    sentiment: LabelPrediction
    priority: LabelPrediction
    model_version: str


class SupportTicketAnalyzer:
    def __init__(self) -> None:
        self.category_classifier = TicketCategoryClassifier()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.priority_predictor = PriorityPredictor()
        self.model_version = get_settings().model_version

    def analyze(self, subject: str, description: str) -> TicketAnalysis:
        text = f"{subject}\n{description}"
        category = self.category_classifier.predict(text)
        sentiment = self.sentiment_analyzer.predict(text)
        priority = self.priority_predictor.predict(text, sentiment.label)
        return TicketAnalysis(
            category=category,
            sentiment=sentiment,
            priority=priority,
            model_version=self.model_version,
        )


analyzer = SupportTicketAnalyzer()
