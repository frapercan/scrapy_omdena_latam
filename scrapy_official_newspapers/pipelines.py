# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os
from scrapy.utils.python import to_bytes

from scrapy.exporters import CsvItemExporter
from sqlalchemy.orm import sessionmaker
from scrapy_official_newspapers.models import Policy, Processing, db_connect, create_table


class ScrapyOfficialNewspapersMySQLPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.session()
        processing = Processing(s3_raw=hashlib.sha1(to_bytes(item['doc_url'])).hexdigest())
        session.add(processing)

        policy = Policy(
            country=item['country'],
            geo_code=item['geo_code'],
            level=item['level'],
            source=item['source'],
            title=item['title'],
            reference=item['reference'],
            authorship=item['authorship'],
            resume=item['resume'],
            publication_date=item['publication_date'],
            enforcement_date=item['enforcement_date'],
            url=item['url'],
            doc_url=item['doc_url'],
            doc_name=item['doc_name'],
            doc_type=item['doc_type'],
            processing = processing
        )
        session.merge(policy)
        session.commit()
