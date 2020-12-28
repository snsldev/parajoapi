# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from celery.utils.log import get_task_logger
from .scrap.CrawlerEncar import CrawlerEncar

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def sayHello():
    logger.info('hello 출력')
    print('hello celery')

# 차량 가격정보 수집하기
@shared_task
def scrapCarPrice():
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarPrice()
