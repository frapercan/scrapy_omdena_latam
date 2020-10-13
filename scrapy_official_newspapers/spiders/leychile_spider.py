import scrapy
import json
from scrapy_official_newspapers.items import ScrapyOfficialNewspapersItem
import datetime
from dateparser import parse

class LeychileSpider(scrapy.Spider):
    name = "leychile"
    num_pag = 2 # determine the number of pages to scrape from the total of 3493 (349.254 legal norms)
    start_urls = [f"https://nuevo.leychile.cl/servicios/buscarjson?itemsporpagina=100&npagina={i}&cadena=" for i in range(1, num_pag)]
    country = "Chile"
    geo_code = "CHL-000-00000-0000000"
    level = "0"
    source = "LeyChile"
    collector = "Ignacio Fernandez"
    scrapper_name = "Ignacio Fernandez"
    scrapable = "True"

    def parse(self, response):
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
            item['reference'] = None
            item['url'] = norm_url
            item['doc_url'] = doc_url
            item['file_urls'] = [doc_url]
            item['doc_name'] = doc_name + '.' + doc_type
            item['doc_type'] = doc_type
            yield item
