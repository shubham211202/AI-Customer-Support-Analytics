from app.ml.classifier import LabelPrediction


class SentimentAnalyzer:
    positive_words = {"thanks", "thank", "great", "good", "helpful", "resolved", "love"}
    negative_words = {
        "angry",
        "bad",
        "broken",
        "disappointed",
        "frustrated",
        "hate",
        "issue",
        "problem",
        "terrible",
        "unable",
        "worst",
    }

    def predict(self, text: str) -> LabelPrediction:
        normalized = text.lower()
        positive_score = sum(1 for word in self.positive_words if word in normalized)
        negative_score = sum(1 for word in self.negative_words if word in normalized)

        if negative_score > positive_score:
            return LabelPrediction("negative", min(0.65 + negative_score * 0.08, 0.95))
        if positive_score > negative_score:
            return LabelPrediction("positive", min(0.65 + positive_score * 0.08, 0.95))
        return LabelPrediction("neutral", 0.6)
