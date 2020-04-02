from .scraper import Scrapper
from .crawlerEncar import CrawlerEncar
from ..models import CarModelDetail

def scaperWorker():
  crawler = CrawlerEncar()
  scraper = Scrapper(crawler)
  scraper.scrap()


# # 차정보 스크래핑
# def scrapCar():
#   #DB의 모든 차량 카테고리 리스트를 불러옴
#   print('START-SCRAPING-CAR-PROCESS =================')
#   carDBList = CarModelDetail.objects.all().select_related().select_related()
#   # print(results)
#   # 웹크롤러 초기화 
#   crawl = Crawler()
#   for modelDetail in carDBList:
#     modelDetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
#     catg_modeldetail_id = modelDetail.seq
#     model = modelDetail.model
#     brand = model.brand
#     print(f"brand: {brand.name}, model: {model.name},  model-detail:{modelDetail_name} ")
#     #엔카에서 스크랩하기
#     scrapedList = searchFromEncar(crawl, brand.name, model.name, modelDetail_name)
#     if scrapedList is not None:
#       storeCarInfo(catg_modeldetail_id, scrapedList)
#     # print(result)
#   print('END-SCRAPING-CAR-PROCESS =================')
#   crawl.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료

# # 차정보 DB에 저장
# def storeCarInfo(catg_modeldetail_id, scrapedList):
#   for item in scrapedList:
#     carinfo = CarInfo(catg_modeldetail_id=catg_modeldetail_id, carId=item.carId, info=item.info, price=item.price, accident=item.accident, site=item.site)
#     carinfo.save()
