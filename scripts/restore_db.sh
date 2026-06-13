#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_backup_file.sql.gz>"
    exit 1
fi

BACKUP_FILE="$1"

# Resolve absolute path on the host
ABS_BACKUP_FILE="$(readlink -f "$BACKUP_FILE" 2>/dev/null || realpath "$BACKUP_FILE")"

if [ ! -f "$ABS_BACKUP_FILE" ]; then
    echo "Error: Backup file '$ABS_BACKUP_FILE' does not exist."
    exit 1
fi

# Get the filename (basename)
FILENAME=$(basename "$ABS_BACKUP_FILE")

# Verify if the file is in the backups directory
# (If not, copy it to the backups directory so the container can access it)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"

if [ "$(dirname "$ABS_BACKUP_FILE")" != "$BACKUP_DIR" ]; then
    echo "Copying backup file to $BACKUP_DIR to make it accessible to container..."
    cp "$ABS_BACKUP_FILE" "$BACKUP_DIR/"
fi

echo "Restoring PostgreSQL database 'support_analytics' from: $FILENAME..."

# Stream gzipped backup inside container using the mounted /backups volume
docker exec support_analytics_db sh -c "gunzip -c /backups/$FILENAME | psql -U postgres -d support_analytics"

echo "Database restoration completed successfully!"
