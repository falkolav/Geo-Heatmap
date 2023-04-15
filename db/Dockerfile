FROM postgis/postgis:15-3.3

RUN apt-get update && \
    apt-get install -y postgis && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5432