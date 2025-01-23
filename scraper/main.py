import os
import sys
import argparse
import subprocess

from scrapy.crawler import CrawlerProcess

from BUScraper.spiders.ConfigSpider import ConfigSpider


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dir", 
        type=str, 
        help="O diretorio em que os BUs serao salvos"
    )

    parser.add_argument(
        "--pleito", 
        type=str, 
        help="O pleito a ser baixado (ou \"todos\")"
    )

    args = parser.parse_args()

    dir = args.dir
    if not dir:
        dir = input("Digite o nome do diretorio em que serao salvos os BUs: ")

    pleito = args.pleito

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