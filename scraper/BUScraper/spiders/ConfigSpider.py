import os
import scrapy
import socket
import itertools
import psutil
import redis
import json

class ConfigSpider(scrapy.Spider):
    name = "ConfigSpider"
    start_urls = [
        "https://resultados.tse.jus.br/oficial/comum/config/ele-c.json",
    ]

    def __init__(self, diretorio, pleito=None, *args, **kwargs):
        super(ConfigSpider, self).__init__(*args, **kwargs)
        self.diretorio = diretorio
        self.pleito = pleito
        self.ufs = ["ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to", "zz"]

        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_queue = redis.Redis(redis_host, redis_port, db=0)
        self.redis_queue.delete('aux_queue')
        
        avail_bind_addr = [addr.address
                                for addr in itertools.chain(*psutil.net_if_addrs().values())
                                if addr.family == socket.AF_INET6 and not addr.address.startswith('f') and addr.address != '::1']
        self.log(f'Available bind address: {avail_bind_addr}')
        self.bind_addr_iter = itertools.cycle(avail_bind_addr)

    # processa o arquivo de configuracao de eleicoes e constroi a url para os arquivos de configuracao de secao
    def parse(self, response):
        ciclo = response.json()['c']
        self.urlBase = f"https://resultados.tse.jus.br/oficial/{ciclo}/arquivo-urna/"
        pleitos = [pleito['cd'] for pleito in response.json()['pl']]

        escolha = self.pleito or ""

        while escolha != "sair":
            if escolha == "":
                print(f"\nPleitos disponiveis: {pleitos}")
                escolha = input(f"Escolha um pleito (ou \'ajuda\'): ")

            if escolha == "todos":
                escolha = "sair"
                for pleito in pleitos:
                    for uf in self.ufs:
                        filename = f"{uf}-p{pleito.zfill(6)}-cs.json"
                        url = self.urlBase + f"{pleito}/config/{uf}/{filename}"
                        yield scrapy.Request(url=url, callback=self.parse_secoes_config, meta={'bindaddress': (next(self.bind_addr_iter), 0)})

            elif escolha == "ajuda":
                escolha = ""
                print("\ncomandos:")
                print("\'ajuda\' - mostra menu de ajuda")
                print("\'todos\' - baixa os BUs de todos os pleitos disponiveis")
                print("\'sair\' - encerra o programa")

            elif escolha in pleitos:
                pleito = escolha
                escolha = "sair"
                for uf in self.ufs:
                    filename = f"{uf}-p{pleito.zfill(6)}-cs.json"
                    url = self.urlBase + f"{pleito}/config/{uf}/{filename}"
                    yield scrapy.Request(url=url, callback=self.parse_secoes_config, meta={'bindaddress': (next(self.bind_addr_iter), 0)})

            elif escolha != "sair":
                escolha = ""
                print("Pleito invalido!")

    # processa os arquivos de configuracao de secao e controi a url para os arquivos auxiliares de secao
    def parse_secoes_config(self, response):
        cdPleito = response.json()['cdp']

        for abrangencia in response.json()['abr']:
            uf = abrangencia['cd'].lower()
            dir = os.getenv("DADOS_DIR", "") + "/" + self.diretorio + "/" + uf + "/"
            os.makedirs(dir, exist_ok=True)

            for municipio in abrangencia['mu']:
                cdMunicipio = municipio['cd'].zfill(5)

                for zona in municipio['zon']:
                    cdZona = zona['cd'].zfill(4)

                    for secao in zona['sec']:
                        if 'nsp' not in secao:
                            nSecao = secao['ns'].zfill(4)

                            filename = f"p{cdPleito.zfill(6)}-{uf}-m{cdMunicipio}-z{cdZona}-s{nSecao}-aux.json"
                            url = self.urlBase + f"{cdPleito}/dados/{uf}/{cdMunicipio}/{cdZona}/{nSecao}/{filename}"
                            item = {'url': url, 'uf': uf}
                            # print(url)
                            self.redis_queue.lpush('aux_queue', json.dumps(item))
