FROM python:2-alpine

MAINTAINER FU YAO & LI YANZHE

WORKDIR /usr/src/app

ADD ./ ./UrlSpider

WORKDIR UrlSpider

RUN pip install -U pip \
    && pip install -r requirements.txt

CMD ["scrapy","crawl","Url","-a","category=http://www.freebuf.com"]
