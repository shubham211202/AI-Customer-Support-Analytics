from datetime import datetime, timedelta
import logging
import psycopg2
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

logger = logging.getLogger(__name__)

def evaluate_prediction_confidence(**context):
    """
    Connects to the PostgreSQL DB, queries recent prediction confidence scores,
    and returns 'trigger_retrain' if average confidence is below 0.75,
    otherwise returns 'skip_retrain'.
    """
    logger.info("Connecting to PostgreSQL database to fetch prediction history...")
    try:
        conn = psycopg2.connect(
            host="db",
            database="support_analytics",
            user="postgres",
            password="postgres",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Select confidence values of the last 50 ticket predictions
        cursor.execute("""
            SELECT category_confidence, sentiment_confidence, priority_confidence 
            FROM ticket_predictions 
            ORDER BY created_at DESC 
            LIMIT 50
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        # If DB query fails, log the error and default to skipping retrain
        return "skip_retrain"

    if not rows:
        logger.info("No predictions found in the database yet. Skipping retraining trigger.")
        return "skip_retrain"

    total_confidence = 0.0
    for row in rows:
        cat_conf, sent_conf, prio_conf = row
        # Average confidence of the individual prediction
        total_confidence += (cat_conf + sent_conf + prio_conf) / 3.0

    avg_confidence = total_confidence / len(rows)
    logger.info(f"Evaluated {len(rows)} recent predictions. Average prediction confidence: {avg_confidence:.4f}")

    threshold = 0.75
    if avg_confidence < threshold:
        logger.warning(f"Average prediction confidence {avg_confidence:.4f} is BELOW threshold ({threshold})!")
        logger.warning("Auto-retraining of models is required.")
        return "trigger_retrain"
    else:
        logger.info(f"Average prediction confidence {avg_confidence:.4f} is ABOVE threshold ({threshold}).")
        logger.info("Models are performing adequately. Skipping retraining.")
        return "skip_retrain"


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    'monitor_and_retrain_pipeline',
    default_args=default_args,
    description='A DAG to monitor average prediction confidence and trigger retraining when accuracy decays',
    schedule_interval=None,
    catchup=False,
) as dag:

    check_confidence = BranchPythonOperator(
        task_id='check_confidence',
        python_callable=evaluate_prediction_confidence,
    )

    trigger_retrain = TriggerDagRunOperator(
        task_id='trigger_retrain',
        trigger_dag_id='train_model_pipeline',
        wait_for_completion=False,
    )

    skip_retrain = EmptyOperator(
        task_id='skip_retrain',
    )

    # Define DAG structure
    check_confidence >> [trigger_retrain, skip_retrain]
