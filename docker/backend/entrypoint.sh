#!/bin/bash

set -e

python /app/backend/src/app.py

exec "$@"