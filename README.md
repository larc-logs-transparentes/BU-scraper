# BU Scraper

Este script realiza o download dos Boletins de Urna (BUs) gerados pelas urnas eletrônicas durante uma eleição, conforme instruções disponíveis [aqui](https://www.tse.jus.br/eleicoes/informacoes-tecnicas-sobre-a-divulgacao-de-resultados).

## Build
Requer `docker-compose` instalado.\
Após clonar o repositório, inicie o build com `docker-compose build`.\
Esse processo baixa e descompacta os BUs das eleições municipais de 2024, juntos de seus metadados (aprox. 2,8 GB), portanto pode levar algum tempo.


## Scraper
Para executar o scraper, basta usar o comando\
`docker-compose run scraper`\
e seguir as instruções.\
\
É possível executar o scraper passando as informações necessárias por linha de comando, na forma\
`docker-compose run scraper --dir <diretorio> --pleito <pleito>`\
\
Há também um script de comparação de BUs, que pode ser executado com o comando\
`python3 comparar_BUs.py <diretorio_1> <diretorio_2>`\
\
O scraper roda em um container Docker e se conecta automaticamente ao banco de dados MongoDB definido no docker-compose. Cada sessão de scraping gera uma nova coleção no banco, nomeada conforme o diretório informado, onde ficam armazenados os metadados dos BUs baixados.\

### Aviso
É comum receber erros 404 ao iniciar o scraper e selecionar o pleito, o que não impede seu funcionamento. Caso o pleito escolhido não tenha ocorrido em determinado estado brasileiro, o servidor do TSE não terá o arquivo de configuração correspondente, resultando em erro. Esses erros são ignorados automaticamente pelo scraper, que processa apenas os arquivos acessíveis.


## Populando logserver
Com o script `populate_db.py` é possível enviar os BUs na ordem cronológica de recebimento a um logserver local, disponível [aqui](https://github.com/larc-logs-transparentes/config/tree/main). É necessário, além dos arquivos de BU baixados, que seus metadados estejam preenchidos no banco de dados, o que pode ser feito rodando o scraper. Após isso, com o logserver rodando, basta executar o script com `python3 populate_db.py` e seguir as instruções.


## Mongosh
É possível consultar e filtrar os BUs baixados e logados no banco de dados (mongodb) por meio do terminal mongosh, com o comando\
`docker-compose run mongosh`\
\
Para consultar as tabelas de BUs de cada sessão de scraping, use o comando `show collections`.\
Para listar todos os BUs de uma tabela, use o comando `db.<nome_da_tabela>.find()`.\
\
É possível filtrar e ordenar buscas concatenando funções. Por exemplo, para ordenar os BUs na ordem cronológica em que foram recebidos, use o comando `db.<nome_da_tabela>.find().sort({ timestamp: 1 })`, e para filtrar somente os BUs com estado "Totalizado" e então ordená-los em ordem cronológica, use o comando `db.<nome_da_tabela>.find({ status: "Totalizado" }).sort({ timestamp: 1 })`