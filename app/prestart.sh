#! /usr/bin/env sh
# Exit in case a command below fails
set -ex

# Enable the code block for db connectivity and migration
python app/app_prestart.py

# Execute DB migration
alembic upgrade head
