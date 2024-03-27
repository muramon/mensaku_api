FROM python:3.7
RUN pip install elasticsearch

WORKDIR /app

ADD feeder-master-db/tokyo_ramen_review_group.csv .

COPY feeder-master-db/ .