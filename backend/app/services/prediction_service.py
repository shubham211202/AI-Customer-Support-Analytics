from app.ml.model_loader import SupportTicketAnalyzer, analyzer
from app.schemas.prediction import PredictionCreate


class PredictionService:
    def __init__(self, ticket_analyzer: SupportTicketAnalyzer = analyzer) -> None:
        self.ticket_analyzer = ticket_analyzer

    def predict(self, *, subject: str, description: str) -> PredictionCreate:
        analysis = self.ticket_analyzer.analyze(subject=subject, description=description)
        return PredictionCreate(
            category=analysis.category.label,
            category_confidence=analysis.category.confidence,
            sentiment=analysis.sentiment.label,
            sentiment_confidence=analysis.sentiment.confidence,
            priority=analysis.priority.label,
            priority_confidence=analysis.priority.confidence,
            model_version=analysis.model_version,
        )
