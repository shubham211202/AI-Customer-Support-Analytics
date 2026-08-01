import re
import string

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class TextPreprocessor:

    def __init__(self):
        self.stopwords = ENGLISH_STOP_WORDS

    def clean_text(self, text):

        if text is None:
            return ""

        text = str(text).lower()

        text = re.sub(r"http\S+", "", text)

        text = re.sub(r"\S+@\S+", "", text)

        text = re.sub(r"\d+", "", text)

        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        text = re.sub(r"\s+", " ", text)

        words = [
            word
            for word in text.split()
            if word not in self.stopwords
        ]

        return " ".join(words)