FROM mongo:4.4.6

RUN rm /etc/apt/sources.list.d/mongodb-org.list \
    && apt-get update \
    && apt-get install -y wget

# baixa e descompacta dados das eleicoes municipais de 2024
RUN mkdir -p /dados_download && \
    wget -P /tmp "https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v1.0/dados.tar.gz.parte_aa" && \
    wget -P /tmp "https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v1.0/dados.tar.gz.parte_ab" && \
    cat /tmp/dados.tar.gz.parte_* > /tmp/dados.tar.gz && \
    tar -xzf /tmp/dados.tar.gz -C /dados_download && \
    rm -rf /tmp/dados.tar.gz*

COPY restore.sh /docker-entrypoint-initdb.d/restore.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /docker-entrypoint-initdb.d/restore.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["mongod"]