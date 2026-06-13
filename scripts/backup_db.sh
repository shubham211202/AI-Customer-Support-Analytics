#!/usr/bin/env bash
set -euo pipefail

# Define backup directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILENAME="db_backup_$TIMESTAMP.sql.gz"

echo "Creating PostgreSQL backup for database 'support_analytics'..."

# Run pg_dump and gzip inside container, writing to the mounted /backups volume
docker exec support_analytics_db sh -c "pg_dump -U postgres -d support_analytics -c --if-exists | gzip > /backups/$BACKUP_FILENAME"

if [ -s "$BACKUP_DIR/$BACKUP_FILENAME" ]; then
    echo "Backup created successfully: $BACKUP_DIR/$BACKUP_FILENAME"
else
    echo "Error: Backup file is empty or failed to generate."
    exit 1
fi
