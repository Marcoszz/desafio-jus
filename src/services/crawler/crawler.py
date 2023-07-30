import scrapy
from scrapy.crawler import CrawlerProcess
import argparse
import re
from json import dumps

class Crawler(scrapy.Spider):
    name = 'crawler'
    start_urls = []
    process_list = []
    degrees = ['primeiro_grau', 'segundo_grau']

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(url, cb_kwargs={'degree': self.degrees[i]})
    
    def parse(self, response, degree):
        process = {
            degree: {
                'classe': response.xpath('//span[@id="classeProcesso"]/text() | //div[@id="classeProcesso"]/span/text()').get(),
                'area': response.xpath('//div[@id="areaProcesso"]/span/text()').get(),
                'assunto': response.xpath('//span[@id="assuntoProcesso"]/text() | //div[@id="assuntoProcesso"]/span/text()').get(),
                'data_distribuicao': response.xpath('//div[@id="dataHoraDistribuicaoProcesso"]/text()').get(),
                'juiz': response.xpath('//span[@id="juizProcesso"]/text()').get(),
                'valor_acao': response.xpath('//div[@id="valorAcaoProcesso"]/text() | //div[@id="valorAcaoProcesso"]/span/text()').get().replace(' ', ''),
                'partes_processo': [],
                'movimentacoes': [],
            }
        }

        self.storage_parts(degree, response, process)
        self.storage_movements(degree, response, process)

        self.process_list.append(process)
        
        
    def storage_parts(self, degree, response, process):
         for tr in response.xpath('//table[@id="tableTodasPartes"]/tr'):
            participation = tr.xpath('.//td/span[@class="mensagemExibindo tipoDeParticipacao"]/text()').get().replace('\xa0', '')
            
            parts = self.format_parts(
                tr.xpath('.//td[@class="nomeParteEAdvogado"]/span/text()').getall(), 
                tr.xpath('.//td[@class="nomeParteEAdvogado"]/text()').getall()
                )

            process[degree]['partes_processo'].append({participation: parts})
    
    def storage_movements(self, degree, response, process):
         for tr in response.xpath('//tbody[@id="tabelaTodasMovimentacoes"]/tr'):
            date = tr.xpath('.//td[contains(@class, "dataMovimentacao")]/text()').get().strip()
            
            movement = self.format_movement(
                tr.xpath('.//td[contains(@class, "descricaoMovimentacao")]/text()').get(), 
                tr.xpath('.//td[contains(@class, "descricaoMovimentacao")]/span/text()').get()
                )

            process[degree]['movimentacoes'].append({date: movement})
    

    def format_parts(self, part_roles, parts):
        parts_formatted = [part.strip() for part in parts if re.search(r'[a-zA-Z]', part)]
        parts_roles_formatted = [part_role.replace('\xa0', ' ').replace('&nbsp', ' ') for part_role in part_roles]
        
        off_set = len(parts_formatted) - len(part_roles)

        parts_with_roles = []
        for i in range(len(parts_formatted)):
            if i >= off_set:
                parts_with_roles.append(parts_roles_formatted[i - off_set] + parts_formatted[i])
            else:
                parts_with_roles.append(parts_formatted[i])

        return parts_with_roles
    
    def format_movement(self, description, details):
        format_info = lambda info: ' '.join(info.strip().split()).replace('\xa0', ' ').replace('&nbsp', ' ') if info is not None else ''
        
        return {
            'descricao': format_info(description),
            'detalhes': format_info(details)
        }
        
if __name__ == "__main__":
    cli = argparse.ArgumentParser()

    cli.add_argument(
        '--urls',
        nargs='*',
        type=str
    )

    args = cli.parse_args()
    
    Crawler.start_urls = args.urls

    process = CrawlerProcess(settings = {'CONCURRENT_REQUESTS':'1'})
    process.crawl(Crawler)
    process.start()

    print(dumps(Crawler.process_list, ensure_ascii=False))