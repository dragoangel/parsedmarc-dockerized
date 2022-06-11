# :e-mail: parsedmarc-dockerized
## :information_source: Info
This stack includes:
- [ParseDMARC](https://domainaware.github.io/parsedmarc/) image to analizing reports (builded from Dockerfile, use pypy image)
- [Elasticsearch & Kibana](https://www.elastic.co/guide/index.html) to store and visualize parsed data
- [Nginx](https://docs.nginx.com/) to handle basic authorization and SSL offloading

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
password = somepassword
```

4. Enable IP geolocation by installing [GeoIP Update software](https://github.com/maxmind/geoipupdate). And edit `docker-compose.yml` to enable access to the MaxMind databases on your host system.
```
volumes:
  - ./parsedmarc/parsedmarc.ini:/etc/parsedmarc.ini:z
  - /path/to/GeoIP:/usr/share/GeoIP
```

5. Create `nginx/htpasswd` to provide Basic-Authentification for Nginx.
In end you will be prompted to enter password to console.
```
docker-compose run nginx htpasswd -c /etc/nginx-secrets/htpasswd anyusername
```

You will be prompted for password.

6. Generate & put your SSL keypair `kibana.crt` and `kibana.key` to `nginx/ssl` folder.

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
docker-compose -up d
```

10. Download & Import Kibana Saved Objects [export.ndjson](https://raw.githubusercontent.com/domainaware/parsedmarc/master/kibana/export.ndjson).

Go to `https://parsedmarc.example.com/app/management/kibana/objects` click on `Import`.

Import downloaded export.ndjson with override.

## Dashboard Sample
![ParceDMARC-Sample](https://github.com/dragoangel/parsedmarc-dockerized/raw/master/ParceDMARC-Sample.png)
