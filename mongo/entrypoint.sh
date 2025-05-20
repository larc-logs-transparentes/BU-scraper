#!/bin/bash
set -e

if [ -d "/dados_download" ]; then
    mv /dados_download/dados/* /dados/
	rm -rf dados_download
fi

exec docker-entrypoint.sh "$@"