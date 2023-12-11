#!/bin/sh
set -e

# Collect system information
# HOSTNAME=$(hostname)
# MAC_ADDRESS=$(ip link show | awk '/ether/ {print $2}' | head -n 1)
# CPU_INFO=$(cat /proc/cpuinfo)
# MEMORY_INFO=$(free -h)
# DISK_INFO=$(df -h)

# Concatenate information and compute SHA-256 hash
# SIGNATURE=$(echo "$HOSTNAME$MAC_ADDRESS$CPU_INFO$MEMORY_INFO$DISK_INFO" | sha256sum | awk '{print $1}')

# Export the variables
# export MACHINE_SIGNATURE=$SIGNATURE

exec gunicorn ailab_apigateway.app:app -w ${GUNICORN_WORKERS:-1} -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:${PORT:-8000} --max-requests 1200 --max-requests-jitter 1000 --access-logfile -
