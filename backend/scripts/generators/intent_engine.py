import random


class IntentEngine:

    def get_intent(self, kb):

        intent = random.choice(kb["intents"])

        return (
            intent["name"],
            random.choice(intent["examples"])
        )