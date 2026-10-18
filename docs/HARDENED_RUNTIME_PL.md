# Parsedmarc Hardening (PL)

Ten dokument opisuje uruchomienie `parsedmarc` w wariancie utwardzonym (hardened), bez zmiany głównego `docker-compose.yml`.

## Co daje `docker-compose.hardened.yml`
Plik nadpisuje tylko usługę `parsedmarc`:
- build z `parsedmarc/Dockerfile.hardened` (distroless runtime)
- root filesystem tylko do odczytu (`read_only: true`)
- `tmpfs` dla `/tmp`
- `no-new-privileges`
- `cap_drop: ALL`
- limity zasobów (`pids_limit`, `mem_limit`, `cpus`)

## Uruchomienie
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml up -d --build parsedmarc
```

## Weryfikacja
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml ps
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml logs -f parsedmarc
```

## Powrót do standardowego obrazu
```bash
sudo docker compose -f docker-compose.yml up -d parsedmarc
```
