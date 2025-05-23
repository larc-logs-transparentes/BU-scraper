import os
import scrapy
import redis
import time
import json

from pathlib import Path
from pymongo import MongoClient
from datetime import datetime

class BUSpider(scrapy.Spider):
    name = "BUSpider"

    def __init__(self, diretorio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diretorio = diretorio
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.redis_client = redis.Redis(redis_host, redis_port, db=0)
        print(self.redis_client.llen('aux_queue'))

        mongo_host = os.getenv("MONGO_HOST", "mongodb://localhost:27017/")
        client = MongoClient(mongo_host)
        db = client["bu"]
        self.colecao = db[self.diretorio]
        
        # PATCHED :(
        # rotacao de enderecos IPv6
        # avail_bind_addr = [addr.address
        #                         for addr in itertools.chain(*psutil.net_if_addrs().values())
        #                         if addr.family == socket.AF_INET6 and not addr.address.startswith('f') and addr.address != '::1']
        # self.log(f'Available bind address: {avail_bind_addr}')
        # self.bind_addr_iter = itertools.cycle(avail_bind_addr)

    def start_requests(self):
        while self.redis_client.llen('aux_queue') > 0:
            item = self.redis_client.rpop('aux_queue')
            if item:
                item = json.loads(item)
                url = item['url']
                uf = item['uf']
                yield scrapy.Request(url, callback=self.parse, meta={'uf': uf})
                # yield scrapy.Request(url, callback=self.parse, meta={'uf': uf, 'bindaddress': (next(self.bind_addr_iter), 0)})
            else:
                time.sleep(5)
    
    # processa os arquivos auxiliares de secao e constroi a url para os BUs
    def parse(self, response):
        urlSecao = response.url.rsplit('/', 1)[0] + '/'
        for hash in response.json()['hashes']:
            cdHash = hash['hash']
            data = hash['dr']
            hora = hash['hr']
            status = hash['st']
            timestamp_string = f"{data} {hora}"
            timestamp = datetime.strptime(timestamp_string, "%d/%m/%Y %H:%M:%S")

            for arquivo in hash['arq']:
                nmArquivo = arquivo['nm']
                tpArquivo = arquivo['tp']

                if tpArquivo == "bu" or tpArquivo == "busa":
                    url = urlSecao + f"{cdHash}/{nmArquivo}"
                    uf = response.meta.get("uf")
                    yield scrapy.Request(url=url, callback=self.parse_bu, meta={'uf': uf, 'timestamp': timestamp, 'status': status})
                    # yield scrapy.Request(url=url, callback=self.parse_bu, meta={'uf': uf, 'timestamp': timestamp, 'status': status, 'bindaddress': (next(self.bind_addr_iter), 0)})

                    # teste para o simulado, que nao gera os BUs
                    # dir = self.diretorio + "/"
                    # Path(f"{dir}/{nmArquivo}").write_bytes("teste".encode())
                    # self.log(f"Arquivo salvo: {nmArquivo}")

    # baixa os BUs
    def parse_bu(self, response):
        filename = response.url.split("/")[-1]
        dir = os.getenv("DADOS_DIR", "./dados") + "/BUs/" + self.diretorio + "/" + response.meta.get("uf") + "/"
        path = dir + filename

        Path(path).write_bytes(response.body)
        # self.log(f"Arquivo salvo: {filename}")

        timestamp = response.meta.get("timestamp")
        status = response.meta.get("status")

        self.colecao.insert_one({"arquivo": filename, "path": path, "url": response.url, "timestamp": timestamp, "status": status})

        # self.entradas_bu.append({"arquivo": filename, "url": response.url, "timestamp": timestamp, "status": status})
        # if len(self.entradas_bu) >= 500:
        #     self.colecao.insert_many(self.entradas_bu)
        #     self.entradas_bu = []

