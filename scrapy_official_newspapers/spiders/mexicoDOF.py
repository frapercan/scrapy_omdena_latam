from scrapy_official_newspapers.spiders import BaseSpider
from scrapy import Request
from scrapy.selector import Selector
from scrapy_official_newspapers.items import ScrapyOfficialNewspapersItem
import time
import re
import datetime



class MexicoDOF(BaseSpider):
    name = "MexicoDOF"
    country = "Mexico"
    geo_code = "MEX-000-00000-0000000"
    level = "0"
    source = "Diario Oficial de la Federacion"
    title = "None"
    url = "https://dof.gob.mx"
    years = [year for year in range(2018, 2020)]
    collector = "Francisco Canales"
    scrapper_name = "Francisco Canales"
    scrapable = "True"
    allowed_domains = ["dof.gob.mx"]
    doc_name = None
    doc_type = 'HTML'


    def create_url_DOF_list(self):
        URLs = []
        for year in self.years:
            for month in range(1, 13):
                for day in range(1, 32):
                    url = self.url + f"/index_113.php?year=" + self.add_leading_zero_two_digits(
                        year) + "&month=" + self.add_leading_zero_two_digits(
                        month) + "&day=" + self.add_leading_zero_two_digits(day)
                    URLs.append(url)
        return URLs

    def start_requests(self):
        for url in self.create_url_DOF_list():
            yield Request(url, dont_filter=True)

    def parse(self, response):
        if len(response.xpath("//*[contains(text(), 'No hay datos para la fecha')]")):
            print("No publication in this date")
            pass
        url = response.url
        year = int(url.split("=")[1][:4])
        month = int(url.split("=")[2][:2])
        day = int(url.split("=")[3][:2])
        date = datetime.datetime(year=year,month=month,day=day)
        item = ScrapyOfficialNewspapersItem()
        trs = response.xpath('/html//td[@class = "subtitle_azul"]')[0].xpath('//tr').xpath(
            'following-sibling::tr[1]')

        authorship = None
        for tr in trs:
            authorship_new = tr.xpath('td[@class = "subtitle_azul"]/text()').get()
            resume_aux = tr.xpath('td/a[@class = "enlaces"]/text()').get()
            url_aux = tr.xpath('td/a[@class = "enlaces"]/@href').get()

            if authorship != authorship_new and authorship_new != None:
                authorship = authorship_new

            if resume_aux and resume_aux != "Ver más":
                resume = resume_aux.replace('\t', '').replace('\n', '')

                doc_url = self.url + url_aux + "&print=true"
                reference = doc_url.split("codigo=")[1][:7]
                item['country'] = self.country
                item['geo_code'] = self.geo_code
                item['level'] = self.level
                item['source'] = self.source
                item['title'] = self.title
                item['reference'] = reference
                item['authorship'] = authorship
                item['resume'] = resume
                item['publication_date'] = date
                item['enforcement_date'] = date
                item['url'] = self.url
                item['doc_url'] = doc_url
                item['doc_name'] = self.doc_name
                item['doc_type'] = self.doc_type
                item['file_urls'] = [doc_url]
                yield item

