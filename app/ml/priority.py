from app.ml.classifier import LabelPrediction


class PriorityPredictor:
    urgent_words = {"urgent", "immediately", "critical", "security", "breach", "down"}
    high_words = {"unable", "failed", "blocked", "locked", "cannot", "can't", "not working"}
    low_words = {"question", "how", "where", "when", "info", "information"}

    def predict(self, text: str, sentiment: str) -> LabelPrediction:
        normalized = text.lower()

        urgent_score = sum(1 for word in self.urgent_words if word in normalized)
        high_score = sum(1 for word in self.high_words if word in normalized)
        low_score = sum(1 for word in self.low_words if word in normalized)

        if urgent_score:
            return LabelPrediction("urgent", min(0.75 + urgent_score * 0.08, 0.98))
        if high_score or sentiment == "negative":
            return LabelPrediction("high", min(0.72 + high_score * 0.06, 0.92))
        if low_score:
            return LabelPrediction("low", min(0.68 + low_score * 0.05, 0.9))
        return LabelPrediction("medium", 0.62)
