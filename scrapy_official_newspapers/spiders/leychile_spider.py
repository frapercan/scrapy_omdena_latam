import scrapy
import json
import datetime
import math
from dateparser import parse
from scrapy_official_newspapers.items import ScrapyOfficialNewspapersItem


class LeychileSpider(scrapy.Spider):
    name = "leychile"
    country = "Chile"
    geo_code = "CHL-000-00000-0000000"
    level = "0"
    source = "LeyChile"
    collector = "Ignacio Fernandez"
    scrapper_name = "Ignacio Fernandez"
    scrapable = "True"

    def __init__(self, date):
        try:
            self.from_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except:
            self.from_date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        date_today = datetime.date.today()
        self.today = date_today.strftime('%Y-%m-%d')
        self.start_urls = [f'https://nuevo.leychile.cl/servicios/Consulta/listaresultadosavanzada?stringBusqueda=-1%23normal%23on%7C%7C4%23normal%23{self.from_date}%23{self.today}%7C%7C117%23normal%23on%7C%7C48%23normal%23on&tipoNormaBA=&npagina=1&itemsporpagina=10&orden=2&tipoviene=4&totalitems=&seleccionado=0&taxonomia=&valor_taxonomia=&o=experta&r=']

    def parse(self, response):
        hits = int(json.loads(response.text)[1]['totalitems'])
        hits = math.ceil(hits/100) + 1
        URLs = [f'https://nuevo.leychile.cl/servicios/Consulta/listaresultadosavanzada?stringBusqueda=-1%23normal%23on%7C%7C4%23normal%23{self.from_date}%23{self.today}%7C%7C117%23normal%23on%7C%7C48%23normal%23on&tipoNormaBA=&npagina={i}&itemsporpagina=100&orden=2&tipoviene=4&totalitems=&seleccionado=0&taxonomia=&valor_taxonomia=&o=experta&r=' for i in range(1, hits)]
        for url in URLs:
            yield scrapy.Request(url, dont_filter=True, callback=self.parse_other)

    def parse_other(self, response):
        item = ScrapyOfficialNewspapersItem()
        for norm in json.loads(response.text)[0]:
            norm_id = norm['IDNORMA']
            norm_url = f'https://www.bcn.cl/leychile/navegar?idNorma={norm_id}'
            doc_name = f'CHL/policy_{norm_id}'
            doc_type = 'pdf'
            publication_date = norm['FECHA_PUBLICACION']
            pub_date_format = parse(publication_date, ['es']).strftime('%Y-%m-%d')
            doc_path = str(norm_id) + '.' + str(pub_date_format) + '.0.0%23'
            doc_url = f'https://nuevo.leychile.cl/servicios/Consulta/Exportar?radioExportar=Normas&exportar_formato={doc_type}&nombrearchivo={doc_name}&exportar_con_notas_bcn=False&exportar_con_notas_originales=False&exportar_con_notas_al_pie=False&hddResultadoExportar={doc_path}'
            item['country'] = self.country
            item['geo_code'] = self.geo_code
            item['level'] = self.level
            item['source'] = self.source
            item['title'] = norm['TITULO_NORMA']
            item['authorship'] = norm['ORGANISMO']
            item['resume'] = norm['DESCRIPCION']
            item['reference'] = norm_id
            item['publication_date'] = pub_date_format
            item['enforcement_date'] = norm['FECHA_PROMULGACION']
            item['url'] = norm_url
            item['doc_url'] = doc_url
            item['doc_name'] = doc_name + '.' + doc_type
            item['doc_type'] = doc_type
            yield item
