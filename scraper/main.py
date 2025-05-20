import argparse
import subprocess

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

    p = subprocess.Popen(['scrapy', 'crawl', 'ConfigSpider', '-a', f'diretorio={dir}', '-a', f'pleito={pleito}'])
    p.wait()

    # dispara n processos para consumir a fila de URLs de arquivos de configuracao
    # inicialmente utilizado com rotatividade de ipv6 para download paralelo de BUs
    # porem, com a retirada do ipv6 dos servidores do TSE, o paralelismo nao e mais vantajoso
    n_spiders = 1
    processes = []
    for _ in range(n_spiders):
        p = subprocess.Popen(['scrapy', 'crawl', 'BUSpider', '-a', f'diretorio={dir}'])
        processes.append(p)

    for p in processes:
        p.wait()