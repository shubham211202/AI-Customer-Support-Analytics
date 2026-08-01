import joblib
import pandas as pd
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from preprocessing import TextPreprocessor

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "generated" / "customer_support_dataset.csv"

MODEL_DIR = BASE_DIR / "saved_models"
MODEL_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape : {df.shape}")

# --------------------------------------------------
# Text Cleaning
# --------------------------------------------------

preprocessor = TextPreprocessor()

df["clean_description"] = (
    df["description"]
    .astype(str)
    .apply(preprocessor.clean_text)
)

# --------------------------------------------------
# Features and Labels
# --------------------------------------------------

X = df["clean_description"]
y = df["category"]

# --------------------------------------------------
# Train/Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

# --------------------------------------------------
# Pipeline
# --------------------------------------------------

pipeline = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42,
            ),
        ),
    ]
)

# --------------------------------------------------
# Train Model
# --------------------------------------------------

print("\nTraining model...\n")

pipeline.fit(X_train, y_train)

print("Training Complete!")

# --------------------------------------------------
# Prediction
# --------------------------------------------------

predictions = pipeline.predict(X_test)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy:.4f}")

print("\nClassification Report\n")

print(classification_report(y_test, predictions))

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, predictions))

# --------------------------------------------------
# Save Model
# --------------------------------------------------

joblib.dump(
    pipeline,
    MODEL_DIR / "ticket_classifier.pkl"
)

print("\nModel Saved Successfully!")