# OpenSearch Setup (EN)

This document describes how to run the local OpenSearch stack from `docker-compose-opensearch.yml`.
The stack creates the `elasticsearch_elastic` Docker network used by `parsedmarc` from the main `docker-compose.yml`.

## What `docker-compose-opensearch.yml` starts
- `opensearch` (ports `9200` and `9600`, published on `127.0.0.1` only)
- `opensearch-dashboards` (port `5601`, published on `127.0.0.1` only; use the `nginx` profile for remote access, or set `OPENSEARCH_BIND_ADDRESS` / `KIBANA_BIND_ADDRESS`)
- optional `nginx` (profile `nginx`, ports `80` and `443`)

## Start OpenSearch
```bash
sudo docker compose -f docker-compose-opensearch.yml up -d
```

## Start OpenSearch + Nginx
```bash
sudo docker compose -f docker-compose-opensearch.yml --profile nginx up -d
```

## Check status
```bash
sudo docker compose -f docker-compose-opensearch.yml ps
sudo docker compose -f docker-compose-opensearch.yml logs -f opensearch opensearch-dashboards
```

## Integration with parsedmarc
After OpenSearch is up, start parser separately:
```bash
sudo docker compose up -d parsedmarc
```

In `parsedmarc/parsedmarc.ini`, the search backend host should point to a service in that network, for example:
```ini
[elasticsearch]
hosts = es01:9200
ssl = False
```

Note: `es01` alias is configured on the `opensearch` service, so existing parsedmarc settings can stay unchanged.

## Stop
```bash
sudo docker compose -f docker-compose-opensearch.yml down
```

## Remove OpenSearch data
```bash
sudo docker compose -f docker-compose-opensearch.yml down -v
```
This removes the `opensearch_data` volume.
