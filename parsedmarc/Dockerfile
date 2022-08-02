FROM docker.io/library/pypy:latest

RUN apt-get update \
    && apt-get install -y libxml2-dev libxslt-dev python3-dev \
    && pip install --no-cache-dir parsedmarc \
    && rm -rf /root/.cache/ \
    && rm -rf /var/lib/{apt,dpkg}/

COPY ./entrypoint.py /
RUN chmod +x /entrypoint.py

ENTRYPOINT ["/entrypoint.py"]
