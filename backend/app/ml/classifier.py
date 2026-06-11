from dataclasses import dataclass


@dataclass(frozen=True)
class LabelPrediction:
    label: str
    confidence: float


class TicketCategoryClassifier:
    keyword_map = {
        "billing": {"invoice", "payment", "charged", "subscription", "bill"},
        "technical_issue": {"error", "bug", "crash", "slow", "failed", "not working"},
        "account_access": {"login", "password", "account", "locked", "access", "reset"},
        "refund": {"refund", "return", "money back", "cancel"},
    }

    def predict(self, text: str) -> LabelPrediction:
        normalized = text.lower()
        scores = {
            category: sum(1 for keyword in keywords if keyword in normalized)
            for category, keywords in self.keyword_map.items()
        }
        category, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            return LabelPrediction(label="general_query", confidence=0.55)
        return LabelPrediction(label=category, confidence=min(0.65 + score * 0.1, 0.95))
