from airflow.models import BaseOperator
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ScrapyOperator(BaseOperator):
    def __init__(self, spider: Spider, **kwargs) -> None:
        super().__init__(task_id=spider.name, **kwargs)
        self.spider = spider

    def execute(self, context):
        extra_settings = context["params"].get("extra_settings", {})

        settings = get_project_settings()
        settings.update(extra_settings)

        process = CrawlerProcess(settings, install_root_handler=False)
        process.crawl(self.spider)
        process.start()
