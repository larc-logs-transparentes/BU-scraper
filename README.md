# BU Scraper

Esse script realiza o download dos Boletins de Urna (BUs) gerados pela urnas eletrônicas durante uma eleição, segundo instruções diponíveis [aqui](https://www.tse.jus.br/eleicoes/informacoes-tecnicas-sobre-a-divulgacao-de-resultados).

## Rodando o scraper
é necessário antes instalar o docker-compose:\
`apt install docker-compose`\
Com o docker-compose instalado, basta executar o comando\
`docker-compose run scraper`\
e seguir as instruções.\
\
É possível executar o scraper passando as informações necessárias por linha de comando, na forma\
`docker-compose run scraper --dir <diretorio> --pleito <pleito>`\
\
Há também um script de comparação de BUs, que pode ser executado com o comando\
`python3 comparar_BUs.py <diretorio_1> <diretorio_2>`


## Consultando banco de dados
É possível consultar e filtrar os BUs baixados e logados no banco de dados (mongodb) por meio do terminal mongosh, com o comando\
`docker-compose run mongosh`\
\
Para consultar as tabelas de BUs de cada sessão de scraping, use o comando `show collections`\
\
Para listar todos os BUs de uma tabela, use o comando `db.<nome_da_tabela>.find()`\
\
É possível filtrar e ordenar buscas concatenando funções. Por exemplo, para ordenar os BUs na ordem cronológica em que foram recebidos, use o comando `db.<nome_da_tabela>.find().sort({ timestamp: 1 })`, e para filtrar somente os BUs com estado "Totalizado" e então ordená-los em ordem cronológica, use o comando `db.<nome_da_tabela>.find({ status: "Totalizado" }).sort({ timestamp: 1 })`


## Populando logserver
Com o script `populate_db.py` é possível enviar os BUs na ordem cronológica de recebimento a um logserver local, disponível [aqui](https://github.com/larc-logs-transparentes/config/tree/main). É necessário, além dos arquivos de BU, seus metadados preenchidos no banco de dados, o que pode ser feito rodando o scraper. Após isso, com o logserver rodando, basta selecionar o nome da coleção de BUs no script e executá-lo com `python3 populate_db.py`