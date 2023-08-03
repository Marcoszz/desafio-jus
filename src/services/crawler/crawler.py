import scrapy
from scrapy.crawler import CrawlerProcess
import argparse
import re
from json import dumps

class Crawler(scrapy.Spider):
    name = 'crawler'
    start_urls = []
    process_list = []
    degrees = ['first_degree', 'second_degree']

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(url, cb_kwargs={'degree': self.degrees[i]})
    
    def parse(self, response, degree):
        process = {
            degree: {
                'class': response.xpath('//span[@id="classeProcesso"]/text() | //div[@id="classeProcesso"]/span/text()').get(),
                'area': response.xpath('//div[@id="areaProcesso"]/span/text()').get(),
                'subject': response.xpath('//span[@id="assuntoProcesso"]/text() | //div[@id="assuntoProcesso"]/span/text()').get(),
                'distribution_date': response.xpath('//div[@id="dataHoraDistribuicaoProcesso"]/text()').get(),
                'judge': response.xpath('//span[@id="juizProcesso"]/text()').get(),
                'share_value': response.xpath('//div[@id="valorAcaoProcesso"]/text() | //div[@id="valorAcaoProcesso"]/span/text()').get(),
                'process_parts': [],
                'movements': [],
            }
        }

        self.storage_parts(degree, response, process)
        self.storage_movements(degree, response, process)
        process[degree]['movements'] = self.group_movements_by_day(degree, process)
        process[degree]['share_value'] = self.format_string(process[degree]['share_value'])

        self.process_list.append(process)     
        
    def storage_parts(self, degree, response, process):
         for tr in response.xpath('//table[@id="tableTodasPartes"]/tr'):
            participation = self.format_string(tr.xpath('.//td/span[@class="mensagemExibindo tipoDeParticipacao"]/text()').get())
            
            parts = self.format_parts(
                tr.xpath('.//td[@class="nomeParteEAdvogado"]/span/text()').getall(), 
                tr.xpath('.//td[@class="nomeParteEAdvogado"]/text()').getall()
                )

            process[degree]['process_parts'].append({participation: parts})
    
    def storage_movements(self, degree, response, process):
         for tr in response.xpath('//tbody[@id="tabelaTodasMovimentacoes"]/tr'):
            date = self.format_string(tr.xpath('.//td[contains(@class, "dataMovimentacao")]/text()').get())
            
            movement = self.format_movement(
                tr.xpath('.//td[contains(@class, "descricaoMovimentacao")]/text()').get(), 
                tr.xpath('.//td[contains(@class, "descricaoMovimentacao")]/a[@class="linkMovVincProc"]/text()').get(),
                tr.xpath('.//td[contains(@class, "descricaoMovimentacao")]/span/text()').get()
                )

            process[degree]['movements'].append({date: movement})

    def format_parts(self, part_roles, parts):
        parts_formatted = [self.format_string(part) for part in parts if re.search(r'[a-zA-Z]', part)]
        parts_roles_formatted = [self.format_string(part_role) for part_role in part_roles]
        
        off_set = len(parts_formatted) - len(part_roles)

        parts_with_roles = [
            parts_roles_formatted[i - off_set] + parts_formatted[i] 
            if i >= off_set 
            else parts_formatted[i]
            for i in range(len(parts_formatted))
            ]

        return parts_with_roles
    
    def format_movement(self, description, link_text, details):
        description_formatted = self.format_string(description)
        link_text_formatted = self.format_string(link_text)
        details_formatted = self.format_string(details)     
        
        if not description_formatted:
            description_formatted = link_text_formatted

        return {
            'description': description_formatted,
            'details': details_formatted
        }

    def format_string(self, string):
        if string is not None:
            return " ".join(string.replace('\xa0', ' ').replace('&nbsp', ' ').strip().split())
        
        return ''

    def group_movements_by_day(self, degree, process_list):
        grouped_movements = []

        for movements in process_list[degree]['movements']:
            for key in movements:
                existing_day = next((item for item in grouped_movements if key in item), None)

                if existing_day:
                    existing_day[key].append(
                        {
                            'description': movements[key]['description'],
                            'details': movements[key]['details']
                        }
                    )
                else:
                    grouped_movements.append(
                        {
                            key: [
                                {
                                    'description': movements[key]['description'],
                                    'details': movements[key]['details']
                                }
                            ]
                        }
                    )

        return grouped_movements
        
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

    print(dumps(Crawler.process_list, ensure_ascii=False).replace("'", "\"").replace("None", "null"))