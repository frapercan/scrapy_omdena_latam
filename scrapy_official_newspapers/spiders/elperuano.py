import scrapy
from scrapy_official_newspapers.items import ScrapyOfficialNewspapersItem
import json


class ElPeruano(scrapy.Spider):
    name = "ElPeruano"
    country = "Peru"
    geo_code = "PER-000-00000-0000000"
    level = "0"
    source = "legislacionforestal.org"
    collector = "Ignacio Fernandez"
    scrapper_name = "Ignacio Fernandez"
    scrapable = "True"
    num_pag = 2 # determine the number of pages to scrape
    start_urls = [f"https://busquedas.elperuano.pe/api/v1/elvis?page={i}&scope=false" for i in range(1, num_pag)]

    def parse(self, response):
        item = ScrapyOfficialNewspapersItem()
        for norm in json.loads(response.text)['hits']:
            item['country'] = self.country
            item['geo_code'] = self.geo_code
            item['level'] = self.level
            item['source'] = self.source
            item['title'] = norm['metadata']['subjectCode']
            item['authorship'] = ''
            item['resume'] = norm['metadata']['description']
            item['reference'] = norm['metadata']['originalDocumentId']
            item['publication_date'] = norm['metadata']['publicationDate']['formatted']
            item['enforcement_date'] = ''
            item['url'] = 'https://busquedas.elperuano.pe' + str(norm['url_link'])
            item['doc_url'] = 'https://busquedas.elperuano.pe/download/url/' + str(norm['metadata']['slug'])
            item['doc_name'] = 'PER/policy_' + norm['metadata']['name']
            item['doc_type'] = 'pdf'

            yield item
