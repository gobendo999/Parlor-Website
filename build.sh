#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# 1. Install all dependencies from requirements.txt
pip install -r requirements.txt

# 2. Collect static files into staticfiles/ directory for WhiteNoise
python manage.py collectstatic --noinput

# 3. Apply all database migrations
python manage.py migrate
