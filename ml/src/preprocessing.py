import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

STOP_WORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """
    Clean customer support ticket text.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def remove_stopwords(text: str) -> str:
    """
    Remove stopwords from the text.
    """
    tokens = text.split()
    filtered_words = [word for word in tokens if word not in STOP_WORDS]
    return " ".join(filtered_words)



"""sample = "My PAYMENT failed yesterday!!! Please help 😡"

cleaned = clean_text(sample)

print(cleaned)

print(remove_stopwords(cleaned))"""