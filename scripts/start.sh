#! /bin/bash
docker compose -f docker/docker-compose.yml  build
docker compose -f docker/docker-compose.yml  up -d
docker compose -f docker/docker-compose.yml exec stock-market-api migrate_db
