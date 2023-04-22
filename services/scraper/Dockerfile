FROM python:3.10.10-bullseye

WORKDIR /scraper

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install scrapy==2.8.0

RUN mkdir -p /srv/scraper
WORKDIR /srv/scraper

ADD . .

RUN chmod 775 start.sh
ENTRYPOINT ["/srv/scraper/start.sh"]

CMD []
