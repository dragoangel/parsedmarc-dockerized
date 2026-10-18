# Konfiguracja ELK (PL)

Ten dokument opisuje uruchomienie lokalnego stacka ELK z pliku `docker-compose-elk.yml`.
Stack tworzy sieć `elasticsearch_elastic`, do której podłącza się `parsedmarc` z głównego `docker-compose.yml`.

## Co uruchamia `docker-compose-elk.yml`
- `elasticsearch` (single-node, port `9200`, wystawiony tylko na `127.0.0.1`)
- `kibana` (port `5601`, wystawiony tylko na `127.0.0.1`)
- opcjonalnie `nginx` (profil `nginx`, porty `80` i `443`)

## Wymagane ustawienia
Ustaw w `.env` zmienne `KIBANA_ENCRYPTEDSAVEDOBJECTS_KEY`, `KIBANA_REPORTING_KEY` i `KIBANA_SECURITY_KEY` (każda min. 32 losowe znaki, np. `openssl rand -hex 32`). Bez nich compose nie uruchomi całego stacku. Przy aktualizacji istniejącego stacku ustaw poprzednie, zahardkodowane wartości, aby zachować odczyt zaszyfrowanych saved objects, a potem zaplanuj rotację.

Elasticsearch i Kibana działają bez uwierzytelniania, więc ich porty są wystawione tylko na `127.0.0.1`. Dostęp zdalny: profil `nginx` (basic auth + TLS) albo świadome ustawienie `ES_BIND_ADDRESS` / `KIBANA_BIND_ADDRESS`.

## Start ELK
```bash
sudo docker compose -f docker-compose-elk.yml up -d
```

## Start ELK + Nginx
```bash
sudo docker compose -f docker-compose-elk.yml --profile nginx up -d
```

## Sprawdzenie stanu
```bash
sudo docker compose -f docker-compose-elk.yml ps
sudo docker compose -f docker-compose-elk.yml logs -f elasticsearch kibana
```

## Integracja z parsedmarc
Po uruchomieniu ELK uruchom parser osobno:
```bash
sudo docker compose up -d parsedmarc
```

W `parsedmarc/parsedmarc.ini` host Elasticsearch powinien wskazywać kontener z tej sieci, np.:
```ini
[elasticsearch]
hosts = es01:9200
ssl = False
```

Uwaga: jeśli używasz wersji TLS/secured Elasticsearch, dostosuj `hosts`, `ssl`, `user`, `password` do swojego środowiska.

## Zatrzymanie
```bash
sudo docker compose -f docker-compose-elk.yml down
```

## Usunięcie danych Elasticsearch
```bash
sudo docker compose -f docker-compose-elk.yml down -v
```
To usunie wolumen `esdata01`.
