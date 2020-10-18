import scrapy
import json
import datetime
import math
from scrapy_official_newspapers.items import ScrapyOfficialNewspapersItem


class ElPeruano(scrapy.Spider):
    name = "ElPeruano"
    country = "Peru"
    geo_code = "PER-000-00000-0000000"
    level = "0"
    source = "busquedas.elperuano.pe"
    collector = "Ignacio Fernandez"
    scrapper_name = "Ignacio Fernandez"
    scrapable = "True"

    def __init__(self, date):
        try:
            self.from_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except:
            self.from_date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        self.from_date = self.from_date.strftime('%d-%m-%Y')
        date_today = datetime.date.today()
        self.today = date_today.strftime('%d-%m-%Y')
        self.start_urls = [f'https://busquedas.elperuano.pe/api/v1/elvis?from_date={self.from_date}&page=0&scope=false&to_date={self.today}']

    def parse(self, response):
        hits = json.loads(response.text)['totalHits']
        hits = math.ceil(hits/10)
        URLs = [f'https://busquedas.elperuano.pe/api/v1/elvis?from_date={self.from_date}&page={i}&scope=false&to_date={self.today}' for i in range(1, hits)]
        for url in URLs:
            yield scrapy.Request(url, dont_filter=True, callback=self.parse_other)

    def parse_other(self, response):
        item = ScrapyOfficialNewspapersItem()
        for norm in json.loads(response.text)['hits']:
            item['country'] = self.country
            item['geo_code'] = self.geo_code
            item['level'] = self.level
            item['source'] = self.source
            item['authorship'] = norm['metadata']['editionName']
            item['resume'] = norm['metadata']['description'].encode('utf-8')
            item['publication_date'] = norm['metadata']['publicationDate']['formatted']
            item['enforcement_date'] = ''
            item['url'] = 'https://busquedas.elperuano.pe' + str(norm['url_link'])
            item['doc_name'] = ('PER/policy_' + norm['metadata']['name'])
            item['doc_type'] = 'pdf'
            try:
                ref = norm['metadata']['subjectCode']
                ref = ref.replace('º', '').replace('°', '').replace(' ', '')
                item['reference'] = ref
            except:
                pass
            try:
                item['title'] = norm['metadata']['slug']
                item['doc_url'] = 'https://busquedas.elperuano.pe/download/url/' + str(norm['metadata']['slug'])
            except:
                pass
            yield item
