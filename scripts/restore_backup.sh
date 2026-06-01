#!/bin/bash -l

docker compose stop

docker run --rm \
  -v n8n_postgres_data:/source \
  -v "$(pwd)":/backups \
  busybox \
  sh -c 'tar -xzvf "$(find ./backups -type f -name "n8n-postgres-*.tar.gz" | sort | tail -n 1)" -C /'

docker run --rm \
  -v n8n_redis_data:/source \
  -v "$(pwd)":/backups \
  busybox \
  sh -c 'tar -xzvf "$(find ./backups -type f -name "n8n-redis-*.tar.gz" | sort | tail -n 1)" -C /'

docker compose start
