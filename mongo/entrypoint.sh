#!/bin/bash

set -e

if [ ! -f "/dados/.initialized" ]; then
	# baixa e reconstroi os dados das eleicoes municipais de 2024
	echo "Baixando arquivo dados.tar.gz.parte_aa"
	wget -P /tmp "https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v0.1/dados.tar.gz.parte_aa"
	echo "Baixando arquivo dados.tar.gz.parte_ab"
	wget -P /tmp "https://github.com/larc-logs-transparentes/BU-scraper/releases/download/v0.1/dados.tar.gz.parte_ab"

	echo "Reconstruindo arquivo"
	cat /tmp/dados.tar.gz.parte_* > /tmp/dados.tar.gz

	echo "Descompactando"
	tar -xzf /tmp/dados.tar.gz -C /tmp

	mv /tmp/dados/* /dados
	
	mv /tmp/mongo_image /dados
	
	touch /dados/.initialized
fi

exec docker-entrypoint.sh "$@"
