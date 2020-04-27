from .Scraper import Scrapper
from .CrawlerEncar import CrawlerEncar
from ..models import CarModelDetail

class ScrapService:

  def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ScrapService, cls).__new__(cls)
        return cls.instance
  
  def scrapCarInfo(self):
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarPriceInfo()

  def scrapCarGrade(self):
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarGradeInfo()
