# BU Scraper

Esse script realiza o download dos Boletins de Urna (BUs) gerados pela urnas eletrônicas durante uma eleição, segundo instruções diponíveis [aqui](https://www.tse.jus.br/eleicoes/informacoes-tecnicas-sobre-a-divulgacao-de-resultados).

## Para rodar em um container
é necessário instalar o docker-compose:\
`apt install docker-compose`,\
e executar o comando\
`docker-compose run shell`\
para subir o container e obter um terminal.\
\
A partir daí é possível rodar os scripts de scraping\
`python3 main.py <diretorio_destino> [pleito=<id>]`\
e de comparação de BUs\
`python3 comparar_BUs.py <diretorio_1> <diretorio_2>`