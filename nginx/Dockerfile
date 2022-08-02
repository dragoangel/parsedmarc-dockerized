from nginx:alpine

RUN apk add --no-cache --virtual .checksum-deps \
    apache2-utils && \
   echo "0 0 * * 0 nginx -s reload" | crontab -
