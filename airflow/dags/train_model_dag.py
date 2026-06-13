from datetime import datetime, timedelta
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator

def train_and_register_models():
    # 1. Define Tracking URI (running in container network)
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("support-ticket-analytics")
    
    # 2. Category Training Data
    categories_data = [
        ("Unable to login with my email", "account_access"),
        ("Cannot reset my password", "account_access"),
        ("Password reset link is not working", "account_access"),
        ("My credit card was charged twice", "billing"),
        ("I need an invoice for my subscription", "billing"),
        ("Where can I find the billing statement?", "billing"),
        ("Payment failed but money was deducted", "billing"),
        ("I want to request a refund for my purchase", "refund"),
        ("Can I cancel my order and get a refund?", "refund"),
        ("How can I return this item?", "refund"),
        ("The website is crashing on login", "technical_issue"),
        ("I found a bug in the dashboard", "technical_issue"),
        ("The app runs very slow today", "technical_issue"),
        ("API call returns a 500 internal server error", "technical_issue"),
        ("General question about features", "general_query"),
    ]
    X_cat = [d[0] for d in categories_data]
    y_cat = [d[1] for d in categories_data]
    
    # 3. Sentiment Training Data
    sentiment_data = [
        ("Thank you so much, this is great!", "positive"),
        ("Resolved very quickly, helpful support", "positive"),
        ("I love using this platform", "positive"),
        ("I am extremely frustrated with this app", "negative"),
        ("This is a terrible experience, very angry", "negative"),
        ("The service is broken and worst support", "negative"),
        ("How do I configure this setting?", "neutral"),
        ("Can you send the documentation?", "neutral"),
        ("What is the status of my ticket?", "neutral"),
    ]
    X_sent = [d[0] for d in sentiment_data]
    y_sent = [d[1] for d in sentiment_data]

    # 4. Priority Training Data
    priority_data = [
        ("URGENT: Database is down and website is crashed", "urgent"),
        ("Critical security vulnerability discovered in our system", "urgent"),
        ("Immediately block my compromised credit card", "urgent"),
        ("Cannot login to my account, password reset fails", "high"),
        ("Failed to download the billing statement", "high"),
        ("The api is slow but working", "medium"),
        ("Where can I view the subscription pricing?", "low"),
        ("How do I change my profile picture?", "low"),
    ]
    X_prio = [d[0] for d in priority_data]
    y_prio = [d[1] for d in priority_data]

    with mlflow.start_run(run_name="train_pipelines"):
        # Log parameters
        mlflow.log_param("vectorizer_ngram_range", (1, 1))
        
        # Train and register Category Model
        cat_pipe = Pipeline([
            ('vectorizer', TfidfVectorizer(lowercase=True, stop_words='english')),
            ('classifier', LogisticRegression(max_iter=1000))
        ])
        cat_pipe.fit(X_cat, y_cat)
        mlflow.sklearn.log_model(
            sk_model=cat_pipe,
            artifact_path="category_model",
            registered_model_name="ticket_category_classifier"
        )
        
        # Train and register Sentiment Model
        sent_pipe = Pipeline([
            ('vectorizer', TfidfVectorizer(lowercase=True, stop_words='english')),
            ('classifier', LogisticRegression(max_iter=1000))
        ])
        sent_pipe.fit(X_sent, y_sent)
        mlflow.sklearn.log_model(
            sk_model=sent_pipe,
            artifact_path="sentiment_model",
            registered_model_name="ticket_sentiment_analyzer"
        )

        # Train and register Priority Model
        prio_pipe = Pipeline([
            ('vectorizer', TfidfVectorizer(lowercase=True, stop_words='english')),
            ('classifier', LogisticRegression(max_iter=1000))
        ])
        prio_pipe.fit(X_prio, y_prio)
        mlflow.sklearn.log_model(
            sk_model=prio_pipe,
            artifact_path="priority_model",
            registered_model_name="ticket_priority_predictor"
        )
        
        print("Models successfully trained and registered in MLflow registry!")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'train_model_pipeline',
    default_args=default_args,
    description='A DAG to train and register support ticket classification models',
    schedule_interval=None,
    catchup=False,
) as dag:

    train_task = PythonOperator(
        task_id='train_and_register',
        python_callable=train_and_register_models,
    )
