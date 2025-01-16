# BU Scraper

Esse script realiza o download dos Boletins de Urna (BUs) gerados pela urnas eletrônicas durante uma eleição, segundo instruções diponíveis [aqui](https://www.tse.jus.br/eleicoes/informacoes-tecnicas-sobre-a-divulgacao-de-resultados).

## Rodando em um container
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


## Rodando em velocidade máxima
Para fazer o scraping o mais rápido possível, é necessário se aproveitar de uma vulnerabilidade nos filtros do servidor do TSE (shhh... `;)`).\
O servidor estabelece um limite de 100 requisições por segundo por endereço IP, porém checa somente pelo endereço completo. Caso tenha acesso a uma faixa de endereços IPv6, é possível
enganar o filtro enviando requisições de endereços diferentes dentro da faixa.\
Para conferir se possui uma faixa disponível, use o comando `ip addr` (somente linux) e procure por algo do tipo:
```
.
.
.
3: <interface>: <NO-CARRIER,BROADCAST,MULTICAST,UP> ...
.
.
.
    inet6 <endereço_IPv6>/64 scope global ...
.
.
.
```
Em caso afirmativo, substitua os valores de IP e nome da interface no script `add_ips` pelos seus e o execute com permissões de admin. Após isso, é só rodar o container e o scraper e esperar os downloads terminarem.\
\
(feature interna apenas, não deve ser publicada)


## Consultando banco de dados
É possível consultar e filtrar os BUs baixados e logados no banco de dados (mongodb) por meio do terminal mongosh, com o comando\
`mongosh mongodb://localhost:8090/bu`\
(A porta 8090 está configurada como padrão para o o banco de dados no arquivo de configuração `docker-compose.yml`. Caso troque a porta no arquivo de configuração, é necessário substituí-la também no comando)\
\
\
Para consultar as tabelas de BUs de cada sessão de scraping, use o comando `show collections`\
\
Para listar todos os BUs de uma tabela, use o comando `db.<nome_da_tabela>.find()`\
\
É possível filtrar e ordenar buscas concatenando funções. Por exemplo, para ordenar os BUs na ordem cronológica em que foram gerados, use o comando `db.<nome_da_tabela>.find().sort({ timestamp: 1 })`, e para filtrar somente os BUs com estado "Totalizado" e então ordená-los em ordem cronológica, use o comando `db.<nome_da_tabela>.find({ status: "Totalizado" }).sort({ timestamp: 1 })`
