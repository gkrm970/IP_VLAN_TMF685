#! /usr/bin/env sh

# Enable the code block for db connectivity and migration


# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py

