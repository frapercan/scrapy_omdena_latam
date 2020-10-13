# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spiders import Spider


class BaseSpider(Spider):
    def parse_date(self, raw_date):
        import re
        date = re.search(r'(\d+/\d+/\d+)', raw_date)
        date = date.group(0)
        return (self.validate_date(date))

    def validate_date(self, date_text):
        from dateutil.parser import parse
        try:
            parse(date_text, dayfirst=True)
            return date_text
        except ValueError as err:
            return err

    def parseHTML_to_txt(self, response):
        from bs4 import BeautifulSoup

        clean_text = ''.join(BeautifulSoup(response, "html.parser").stripped_strings)

    def add_leading_zero_two_digits(self, number):
        if number < 10:
            num = "0" + str(number)
        else:
            num = str(number)
        return (num)


