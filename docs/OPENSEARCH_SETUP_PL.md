# Konfiguracja OpenSearch (PL)

Ten dokument opisuje uruchomienie lokalnego stacka OpenSearch z pliku `docker-compose-opensearch.yml`.
Stack tworzy sieć `elasticsearch_elastic`, do której podłącza się `parsedmarc` z głównego `docker-compose.yml`.

## Co uruchamia `docker-compose-opensearch.yml`
- `opensearch` (porty `9200` i `9600`, wystawione tylko na `127.0.0.1`)
- `opensearch-dashboards` (port `5601`, tylko `127.0.0.1`; dostęp zdalny przez profil `nginx` lub `OPENSEARCH_BIND_ADDRESS` / `KIBANA_BIND_ADDRESS`)
- opcjonalnie `nginx` (profil `nginx`, porty `80` i `443`)

## Start OpenSearch
```bash
sudo docker compose -f docker-compose-opensearch.yml up -d
```

## Start OpenSearch + Nginx
```bash
sudo docker compose -f docker-compose-opensearch.yml --profile nginx up -d
```

## Sprawdzenie stanu
```bash
sudo docker compose -f docker-compose-opensearch.yml ps
sudo docker compose -f docker-compose-opensearch.yml logs -f opensearch opensearch-dashboards
```

## Integracja z parsedmarc
Po uruchomieniu OpenSearch uruchom parser osobno:
```bash
sudo docker compose up -d parsedmarc
```

W `parsedmarc/parsedmarc.ini` host wyszukiwarki powinien wskazywać usługę w tej samej sieci, np.:
```ini
[elasticsearch]
hosts = es01:9200
ssl = False
```

Uwaga: alias `es01` jest zdefiniowany na usłudze `opensearch`, więc obecna konfiguracja `parsedmarc` może pozostać bez zmian.

## Zatrzymanie
```bash
sudo docker compose -f docker-compose-opensearch.yml down
```

## Usunięcie danych OpenSearch
```bash
sudo docker compose -f docker-compose-opensearch.yml down -v
```
To usunie wolumen `opensearch_data`.
