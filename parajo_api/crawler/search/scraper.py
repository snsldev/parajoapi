from ..models import CarModelDetail, CarInfo
from .crawlerEncar import CrawlerEncar
import re

'''
차량 카테고리 db에서 모든 리스트를 가져와서 
하나씩 스크랩핑해서
carinfo db에 삽입한다
'''

class Scrapper:

  def __init__(self, crawler):
    self.crawler = crawler

  # 차정보 스크래핑
  def scrap(self):
    #DB의 모든 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-PROCESS =================')
    carDBList = CarModelDetail.objects.all().select_related().select_related()
    # print(results)
    crawler = self.crawler
    for modelDetail in carDBList:
      modelDetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      catg_modeldetail_id = modelDetail.seq
      model = modelDetail.model
      brand = model.brand
      print(f"brand: {brand.name}, model: {model.name},  model-detail:{modelDetail_name} ")
      #스크랩하기
      scrapedList = crawler.search(brand.name, model.name, modelDetail_name)
      if scrapedList is not None:
        self.storeCarInfo(catg_modeldetail_id, scrapedList)
      # print(result)
    print('END-SCRAPING-CAR-PROCESS =================')
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
  
  # 차정보 DB에 저장
  def storeCarInfo(self, catg_modeldetail_id, scrapedList):
    for item in scrapedList:
      carinfo = CarInfo(catg_modeldetail_id=catg_modeldetail_id, carId=item.carId, info=item.info, price=item.price, accident=item.accident, site=item.site)
      carinfo.save()
