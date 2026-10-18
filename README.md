# :e-mail: parsedmarc-dockerized

## ⏱️ Archive Notice
domainaware/parsedmarc now provide own official docker images and compose examples, please use them instead.

## :information_source: Info
This stack includes:
- [ParseDMARC](https://domainaware.github.io/parsedmarc/) image to analizing reports (builded from Dockerfile, use pypy image)
- [Elasticsearch & Kibana](https://www.elastic.co/guide/index.html) to store and visualize parsed data
- [Nginx](https://docs.nginx.com/) to handle basic authorization and SSL offloading

Additional docs:
- [MSGRAPH_TOKEN_SETUP.md](MSGRAPH_TOKEN_SETUP.md) - configuration of MS Graph token refresh using `client secret` and `certificate`
- [docs/ELK_SETUP_PL.md](docs/ELK_SETUP_PL.md) - uruchomienie i integracja ELK (PL)
- [docs/ELK_SETUP_EN.md](docs/ELK_SETUP_EN.md) - ELK startup and integration guide (EN)
- [docs/OPENSEARCH_SETUP_PL.md](docs/OPENSEARCH_SETUP_PL.md) - uruchomienie i integracja OpenSearch (PL)
- [docs/OPENSEARCH_SETUP_EN.md](docs/OPENSEARCH_SETUP_EN.md) - OpenSearch startup and integration guide (EN)
- [docs/HARDENED_RUNTIME_PL.md](docs/HARDENED_RUNTIME_PL.md) - uruchomienie parsedmarc w trybie hardened (PL)
- [docs/HARDENED_RUNTIME_EN.md](docs/HARDENED_RUNTIME_EN.md) - run parsedmarc in hardened mode (EN)

## :rocket: Quick Start (MS Graph token refresh)
1. Prepare env:
```bash
cp .env.example .env
```
2. Fill `.env` (`TENANT_ID`, `CLIENT_ID`; for certificate also `MSGRAPH_CERT_THUMBPRINT`).
3. Start parsedmarc:
```bash
sudo docker compose up -d parsedmarc
```

### Variant A: client secret
```bash
printf '%s' 'TU_WKLEJ_CLIENT_SECRET' > secrets/msgraph_client_secret.txt
chmod 600 secrets/msgraph_client_secret.txt
sudo docker compose --profile msgraph-secret up -d --build msgraph-token-refresh-secret
```

### Variant B: certificate
```bash
chmod 600 secrets/msgraph_client_certificate.pem
chmod 644 secrets/msgraph_client_certificate_public.pem
sudo docker compose --profile msgraph-cert up -d --build msgraph-token-refresh-cert
```

Token output file (both variants):
```bash
sudo docker compose exec msgraph-token-refresh-secret sh -c 'ls -l /tokens/.token.json && tail -n +1 /tokens/.token.json'
```

## :shield: Security note
Please note that the Fail2Ban technique is not implemented, so posting this project on the Internet :globe_with_meridians: can be risky. 

You yourself are responsible for your actions.

The author recommends restricting Nginx access only to trusted IP addresses.

The project is delivered as is without any warranty.

To update parsedmarc:
```
cd parsedmarc-dockerized
docker-compose build --no-cache --pull parsedmarc
docker-compose pull
docker-compose up -d
```

## :gear: How-to deploy from scratch
First of all you need to have :whale: Docker and :octocat: Docker Compose.

1. Learn how to install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/).
Quick installation for most operation systems:
- Docker
```
curl -sSL https://get.docker.com/ | CHANNEL=stable sh
# After the installation process is finished, you may need to enable the service and make sure it is started (e.g. CentOS 7)
systemctl enable docker.service
systemctl start docker.service
```
- Docker-Compose
```
curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-Linux-x86_64 > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

2. Clone the master branch of the repository.
```
git clone https://github.com/dragoangel/parsedmarc-dockerized
cd parsedmarc-dockerized
```

3. Change `[imap]` configuration and tweak `parsedmarc/parsedmarc.ini` to your needs.
Syntax and description avaible [here](https://domainaware.github.io/parsedmarc/index.html#configuration-file)
```
[imap]
host = imap.example.com
user = parsedmarc@example.com
```

Keep the password out of `parsedmarc.ini`, which is tracked in git. Put it in `.env` (gitignored) instead, and `docker-compose.yml` passes it to the container:
```
PARSEDMARC_IMAP_PASSWORD=somepassword
```
`.env.example` lists the other supported secrets (Elasticsearch, OpenSearch, Microsoft Graph).

4. Enable IP geolocation by installing [GeoIP Update software](https://github.com/maxmind/geoipupdate). And edit `docker-compose.yml` to enable access to the MaxMind databases on your host system.
```
volumes:
  - ./parsedmarc/parsedmarc.ini:/etc/parsedmarc.ini:z
  - /path/to/GeoIP:/usr/share/GeoIP
```

5. Create `nginx/htpasswd` to provide Basic-Authentification for Nginx.
Change `dnf` to your package manager and `anyusername` to your needs.
In end you will be prompted to enter password to console.
```
dnf install -y httpd-tools
htpasswd -c nginx/htpasswd anyusername
```

6. Generate & put your SSL keypair `kibana.crt` and `kibana.key` to `nginx/ssl` folder. Everything in `nginx/ssl/` and `nginx/htpasswd` is gitignored, so the key and the password hashes cannot be committed by accident.

There are to many posible solutuins like [Let's Encrypt](https://letsencrypt.org/docs/client-options/), private PKI or [self-hosted](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04) certificates.

It all up to you what to use. Note: for Let's Encrypt you need modify nginx configs to support it. You can use local ACME or modify docker-compose image. 

7. Create needed folders and configure permissions.
```
mkdir -p elasticsearch/data
chown 1000:0 elasticsearch/data
chmod 755 elasticsearch/data
chown -R 0:101 nginx/*
chmod 640 nginx/htpasswd
chmod 640 nginx/ssl/kibana.key
```

8. Tune `vm.max_map_count` on your OS, original how-to avaible [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).

9. Start stack.
```
docker-compose up -d
```

10. Download & Import Kibana Saved Objects [export.ndjson](https://raw.githubusercontent.com/domainaware/parsedmarc/master/kibana/export.ndjson).

Go to `https://parsedmarc.example.com/app/management/kibana/objects` click on `Import`.

Import downloaded export.ndjson with override.

## Dashboard Sample
![ParceDMARC-Sample](https://github.com/dragoangel/parsedmarc-dockerized/raw/master/ParceDMARC-Sample.png)
