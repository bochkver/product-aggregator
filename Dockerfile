FROM debian:bullseye-slim

ENV LANG C.UTF-8

RUN set -ex \
  && apt-get -y update \
  && apt-get -y upgrade

RUN apt-get -y install\
  python3 \
  python3-pip \
  git

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./product_aggregator /app/test_task/product_aggregator
COPY ./product_aggregator.py /app/test_task/product_aggregator.py
COPY ./etc /conf

WORKDIR /app/test_task

CMD ["python3", "/app/test_task/product_aggregator.py", "-c", "/conf/product_aggregator.conf"]
