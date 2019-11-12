# parsedmarc-dockerized
## Info
This stack includes:
- [ParseDMARC](https://domainaware.github.io/parsedmarc/) image to analizing reports (builded from Dockerfile, use pypy image)
- [Elasticsearch & Kibana](https://www.elastic.co/guide/index.html) to store and visualize parsed data
- [Nginx](https://docs.nginx.com/) to handle basic authorization and SSL offloading

## How-to deploy from scratch
You need Docker and Docker Compose.

1\. Learn how to install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/).
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
curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-Linux-x86_64 > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

2\. Clone the master branch of the repository.
```
git clone https://github.com/dragoangel/parsedmarc-dockerized
cd parsedmarc-dockerized
```

3\. Change `[imap]` configuration and tweak `parsedmarc/parsedmarc.ini` to your needs.
Syntax and description avaible [here](https://domainaware.github.io/parsedmarc/index.html#configuration-file)
```
[imap]
host = imap.example.com
user = parsedmarc@example.com
password = somepassword
```

4\. Create `nginx/htpasswd` to provide Basic-Authentification for Nginx.
Change `dnf` to your package manager and `anyusername` to your needs.
In end you will be promtet to enter password to console.
```
dnf install -y httpd-tools
htpasswd -c nginx/htpasswd anyusername
```

5\. Generate `kibana.crt` and `kibana.key` to `nginx/ssl` folder.
There are many posible solutuins like [Let's Encrypt](https://letsencrypt.org/docs/client-options/), private PKI or [self-hosted](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04) certificates. It all up to you what to use.

6\. Create needed folders and configure permissions.
```
mkdir -p elasticsearch/data
chown 1000:0 elasticsearch/data
chmod 755 elasticsearch/data
chown -R 0:101 nginx/*
chmod 640 nginx/htpasswd
chmod 640 nginx/ssl/kibana.key
```

7\. Tune `vm.max_map_count` on your OS, original how-to avaible [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).

8\. Start stack.
```
docker-compose -up d
```

9\. Download & Import [kibana_saved_objects.json](https://raw.githubusercontent.com/domainaware/parsedmarc/master/kibana/kibana_saved_objects.json).

Go to `https://parsedmarc.example.com/app/kibana#/management/kibana/objects?_g=()` click on `Import`.

Import downloaded kibana_saved_objects.json with override.
