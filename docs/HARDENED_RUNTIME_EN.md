# Parsedmarc Hardening (EN)

This document describes how to run `parsedmarc` in a hardened mode without changing the main `docker-compose.yml`.

## What `docker-compose.hardened.yml` does
It overrides only the `parsedmarc` service:
- build from `parsedmarc/Dockerfile.hardened` (distroless runtime)
- read-only root filesystem (`read_only: true`)
- `tmpfs` for `/tmp`
- `no-new-privileges`
- `cap_drop: ALL`
- resource limits (`pids_limit`, `mem_limit`, `cpus`)

## Start
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml up -d --build parsedmarc
```

## Verify
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml ps
sudo docker compose -f docker-compose.yml -f docker-compose.hardened.yml logs -f parsedmarc
```

## Roll back to standard image
```bash
sudo docker compose -f docker-compose.yml up -d parsedmarc
```
