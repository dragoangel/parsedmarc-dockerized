# ELK Setup (EN)

This document describes how to run the local ELK stack from `docker-compose-elk.yml`.
The stack creates the `elasticsearch_elastic` Docker network used by `parsedmarc` from the main `docker-compose.yml`.

## What `docker-compose-elk.yml` starts
- `elasticsearch` (single-node, port `9200`, published on `127.0.0.1` only)
- `kibana` (port `5601`, published on `127.0.0.1` only)
- optional `nginx` (profile `nginx`, ports `80` and `443`)

## Required settings
Set `KIBANA_ENCRYPTEDSAVEDOBJECTS_KEY`, `KIBANA_REPORTING_KEY` and `KIBANA_SECURITY_KEY` in `.env` (32+ random characters each, e.g. `openssl rand -hex 32`). Without them Compose refuses to start the stack. If you are upgrading an existing stack, set them to the previous hardcoded values to keep existing encrypted saved objects readable, then plan a rotation.

Elasticsearch and Kibana run without authentication, so their ports are bound to `127.0.0.1`. For remote access use the `nginx` profile (basic auth + TLS), or set `ES_BIND_ADDRESS` / `KIBANA_BIND_ADDRESS` if you understand the exposure.

## Start ELK
```bash
sudo docker compose -f docker-compose-elk.yml up -d
```

## Start ELK + Nginx
```bash
sudo docker compose -f docker-compose-elk.yml --profile nginx up -d
```

## Check status
```bash
sudo docker compose -f docker-compose-elk.yml ps
sudo docker compose -f docker-compose-elk.yml logs -f elasticsearch kibana
```

## Integration with parsedmarc
After ELK is up, start parser separately:
```bash
sudo docker compose up -d parsedmarc
```

In `parsedmarc/parsedmarc.ini`, Elasticsearch host should point to the container in that network, e.g.:
```ini
[elasticsearch]
hosts = es01:9200
ssl = False
```

Note: if you use TLS/secured Elasticsearch, adjust `hosts`, `ssl`, `user`, and `password` for your environment.

## Stop
```bash
sudo docker compose -f docker-compose-elk.yml down
```

## Remove Elasticsearch data
```bash
sudo docker compose -f docker-compose-elk.yml down -v
```
This removes the `esdata01` volume.
