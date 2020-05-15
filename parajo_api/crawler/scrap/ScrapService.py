from .Scraper import Scrapper
from .CrawlerEncar import CrawlerEncar
from ..models import CarModelDetail

class ScrapService:

  def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ScrapService, cls).__new__(cls)
        return cls.instance
  
  # 차량 가격정보 수집하기
  def scrapCarPriceService(self):
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarPrice()

  # 차량 카테고리-등급 수집하기
  def scrapCarGradeService(self):
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarGrade()

    
  # 차량 카테고리-등급-세부등급1 수집하기
  def scrapCarGradeSubGroupService(self):
    crawler = CrawlerEncar()
    scraper = Scrapper(crawler)
    scraper.scrapCarGradeSubGroup()

