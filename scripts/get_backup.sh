#!/bin/bash -l

docker compose stop

docker run --rm \
  -v n8n_postgres_data:/source \
  -v $(pwd)/backups:/backup busybox \
  tar -czvf /backup/n8n-postgres-$(date +"%Y-%m-%d").tar.gz -C / source

docker run --rm \
  -v n8n_redis_data:/source \
  -v $(pwd)/backups:/backup busybox \
  tar -czvf /backup/n8n-redis-$(date +"%Y-%m-%d").tar.gz -C / source

docker compose start