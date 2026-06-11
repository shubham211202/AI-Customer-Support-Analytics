# Phase 1 Architecture

Phase 1 builds the backend foundation for the web application:

- FastAPI backend
- PostgreSQL persistence
- Ticket classification
- Sentiment analysis
- Priority prediction
- Tests and documentation

## Layers

```text
app/api          HTTP routing and dependencies
app/schemas      Pydantic request and response models
app/services     Business workflows
app/repositories Database operations
app/models       SQLAlchemy ORM models
app/ml           Prediction interfaces and baseline implementations
app/db           Database engine, sessions, metadata
app/core         Settings and cross-cutting utilities
```

Routes should stay thin. They validate and hand work to services. Services
coordinate repositories and ML components. Repositories hide SQLAlchemy query
details from the rest of the app.

## Database Schema

### tickets

```text
id UUID primary key
customer_id nullable string
subject string
description text
source string
status string
created_at timestamp
updated_at timestamp
deleted_at nullable timestamp
```

### ticket_predictions

```text
id UUID primary key
ticket_id UUID foreign key -> tickets.id
category string
category_confidence float
sentiment string
sentiment_confidence float
priority string
priority_confidence float
model_version nullable string
created_at timestamp
```

Relationship:

```text
tickets 1 ---- many ticket_predictions
```

This prepares the system for MLflow model versioning because one ticket can be
re-predicted by newer models over time.

## Baseline AI Models

Phase 1 uses deterministic rule-based predictors. This gives stable behavior
while we build the production API and database foundation. In Phase 3, MLflow and
Airflow will replace the internals with trained, tracked, registered models.
