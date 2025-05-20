#!/bin/bash

if [ -d "/dados/mongo_image" ]; then
    echo "Restaurando banco de dados"
    mongorestore /dados/mongo_image
else
    echo "Imagem nao encontrada, pulando restauracao"
fi