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


### Observação
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
