#!/bin/bash

# Get the name of the current working directory
current_dir=$(basename "$PWD")

# Check if the current directory is NOT "backend"
if [ "$current_dir" != "backend" ]; then
    echo "Error: You are currently in '$current_dir'. Please change your path to the 'backend' directory before running Celery Beat." >&2
    exit 1
else
    # Execute the Celery command
    celery -A celery_utils.celery_main worker --loglevel=info
fi