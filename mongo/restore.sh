#!/bin/bash

set -e

# baixa e reconstroi os dados das eleicoes municipais de 2024
curl -L -o /tmp/dados.tar.gz.parte_aa https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v0.1/dados.tar.gz.parte_aa
curl -L -o /tmp/dados.tar.gz.parte_ab https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v0.1/dados.tar.gz.parte_ab

cat /tmp/dados.tar.gz.parte_* > /tmp/dados.tar.gz

tar -xzf /tmp/dados.tar.gz -C /tmp

mv /tmp/dados /dados

mongorestore /tmp/mongo_image
