FROM pypy:latest

RUN apt-get update \
    && apt-get install -y libxml2-dev libxslt-dev python3-dev \
    && pip install parsedmarc \
    && rm -rf /root/.cache/ \
    && rm -rf /var/lib/{apt,dpkg}/

CMD ["parsedmarc"]
