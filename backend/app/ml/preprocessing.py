"""
AI Customer Support Analytics Platform

Text Preprocessing Module

This module contains reusable preprocessing functions
used during both model training and inference.
"""

import re
import string

import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# -------------------------------------
# Download required NLTK resources
# (Safe to call multiple times)
# -------------------------------------

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# -------------------------------------
# Initialize
# -------------------------------------

STOP_WORDS = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


# -------------------------------------
# Lowercase
# -------------------------------------

def lowercase(text: str) -> str:
    """
    Convert text to lowercase.
    """

    return text.lower()


# -------------------------------------
# Remove Punctuation
# -------------------------------------

def remove_punctuation(text: str) -> str:
    """
    Remove punctuation from text.
    """

    return text.translate(
        str.maketrans("", "", string.punctuation)
    )


# -------------------------------------
# Remove Numbers
# -------------------------------------

def remove_numbers(text: str) -> str:
    """
    Remove digits from text.
    """

    return re.sub(r"\d+", "", text)


# -------------------------------------
# Tokenization
# -------------------------------------

def tokenize(text: str):
    """
    Convert sentence into list of words.
    """

    return word_tokenize(text)


# -------------------------------------
# Stopword Removal
# -------------------------------------

def remove_stopwords(tokens):
    """
    Remove English stopwords.
    """

    return [
        word
        for word in tokens
        if word not in STOP_WORDS
    ]


# -------------------------------------
# Lemmatization
# -------------------------------------

def lemmatize(tokens):
    """
    Convert words into base form.
    """

    return [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]


# -------------------------------------
# Complete Pipeline
# -------------------------------------

def preprocess(text: str) -> str:
    """
    Complete preprocessing pipeline.

    Steps:
        1. Lowercase
        2. Remove punctuation
        3. Remove numbers
        4. Tokenize
        5. Remove stopwords
        6. Lemmatize
        7. Join back into sentence
    """

    text = lowercase(text)

    text = remove_punctuation(text)

    text = remove_numbers(text)

    tokens = tokenize(text)

    tokens = remove_stopwords(tokens)

    tokens = lemmatize(tokens)

    return " ".join(tokens)


# -------------------------------------
# Test
# -------------------------------------

if __name__ == "__main__":

    sample = (
        "I have been trying to access my account since yesterday "
        "using Google Chrome on my Windows Laptop running Windows 11."
    )

    print("=" * 80)
    print("Original")
    print(sample)

    print()

    print("=" * 80)
    print("Processed")
    print(preprocess(sample))