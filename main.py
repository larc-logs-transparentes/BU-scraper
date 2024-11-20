import os
import sys
import subprocess

from scrapy.crawler import CrawlerProcess

from BUScraper.spiders.ConfigSpider import ConfigSpider


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Uso: python3 baixar_BUs.py <diretorio_destino> [pleito=<id>]')
        exit(1)

    dir = sys.argv[1]
    os.makedirs(dir, exist_ok=True)

    pleito = None
    if len(sys.argv) > 2 and sys.argv[2].startswith("pleito="):
        pleito = sys.argv[2].split("=")[1]

    process = CrawlerProcess(settings={
        'CONCURRENT_REQUESTS': 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
        'DOWNLOAD_DELAY': 0,
        'AUTOTHROTTLE_ENABLED': False,
        "DNS_RESOLVER": "resolver.ForceIPv6Resolver",
        'LOG_LEVEL': 'INFO',
        'REACTOR_THREADPOOL_MAXSIZE': 64,
        'DOWNLOADER_HTTP2_ENABLED': True,
    })
    scraper = process.crawl(ConfigSpider, diretorio=dir, pleito=pleito)
    process.start()
    process.stop()

    processes = []
    for _ in range(8):
        p = subprocess.Popen(['scrapy', 'crawl', 'BUSpider', '-a', f'diretorio={dir}'])
        processes.append(p)

    for p in processes:
        p.wait()