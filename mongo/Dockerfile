FROM mongo:4.4.6

RUN apt-get update && apt-get install -y curl

COPY image /image

COPY restore.sh /docker-entrypoint-initdb.d/restore.sh
RUN chmod +x /docker-entrypoint-initdb.d/restore.sh

