import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logging() -> None:
    log_format = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    
    # Configure root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Check if handlers are already set up to avoid duplication
    if not root_logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(console_handler)
        
    # Rotating File Handler for Promtail/Loki log aggregation
    log_dir = "/app/logs"
    try:
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "backend.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Explicitly configure loggers to capture FastAPI and Uvicorn requests
        for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
            logger = logging.getLogger(logger_name)
            logger.addHandler(file_handler)
            logger.propagate = True
    except Exception as e:
        # Fallback if logs directory is not writable during local testing outside container
        logging.warning(f"Could not configure file log handler: {e}")

