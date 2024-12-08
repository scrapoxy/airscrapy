# Scrapy contrib for Airflow

## Installation

```shell
pip install airscrapy
```


## Airflow Operator

This operator runs Scrapy directly within the worker process
by invoking the Scrapy engine directly, eliminating the need for a separate process.


### Example

If the spider is structured as follows:

```python
import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = [ "http://example.com" ]

    def parse(self, response):
        yield {
            'text': response.css('.info').extract_first()
        }
```

Here’s how you can create a DAG using the operator:

```python
from airflow import DAG
from airscrapy import ScrapyOperator
from myscrapers.spiders.example import ExampleSpider
import os

with DAG(
    dag_id="scrapers",
        # Add extra settings like credentials or token
        params={
            "extra_settings": {
                "CONCURRENT_REQUESTS": 2,
            }
        },
) as dag:
    # Import the shared settings file
    os.environ["SCRAPY_SETTINGS_MODULE"] = "myscrapers.settings"

    task = ScrapyOperator(spider=ExampleSpider)

if __name__ == "__main__":
    dag.test()
```

The `extra_settings` parameter is used to dynamically include elements
such as credentials or tokens, complementing the settings.py file.

Additionally, ensure you set the `SCRAPY_SETTINGS_MODULE` environment variable. 
Without it, Scrapy won't be able to locate the settings.

The DAG directory is organized as follows:

```
dags
|- myscrapers
   |- spiders
      |- __init__.py
      |- example.py
   |- __init__.py
   |- items.py
   |- middlewares.py
   |- pipelines.py
   |- settings.py
|- mydag.py
|- scrapy.cfg
```

This structure enables us to run the DAG in local debugging mode:

```python
python mydag.py
```