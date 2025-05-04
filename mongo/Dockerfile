FROM mongo:4.4.6

RUN rm /etc/apt/sources.list.d/mongodb-org.list \
    && apt-get update \
    && apt-get install -y wget

COPY restore.sh /docker-entrypoint-initdb.d/restore.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /docker-entrypoint-initdb.d/restore.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["mongod"]
