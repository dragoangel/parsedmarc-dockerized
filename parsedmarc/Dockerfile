FROM pypy:3.6-slim

ENV PARSEDMARC_VERSION 6.5.4
RUN apt-get update \
    && apt-get install -y gcc \
    && pip install -y parsedmarc \
    && rm -rf /root/.cache/ \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg}/

CMD ["parsedmarc"]