#!/bin/bash
set -e

PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}
WORKERS=${WORKERS:-2}
RUNTIME_THREADS=${RUNTIME_THREADS:-1}

granian \
  --interface asginl \
  --host "$HOST" \
  --port "$PORT" \
  --workers "$WORKERS" \
  --runtime-threads "$RUNTIME_THREADS" \
  --loop uvloop \
  --log-level info \
  protobuf_django.asgi:application \
