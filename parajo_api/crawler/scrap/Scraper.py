from ..models import CarModelDetail, CarInfo, CarGrade, CarGradeSubGroup
from .CrawlerEncar import CrawlerEncar
import re

'''
스크랩퍼는 정형화 된 데이터를 본사DB에 저장하는 역할을 수행
'''
class Scrapper:

  def __init__(self, crawler: CrawlerEncar):
    self.crawler = crawler

  # 카테고리- 등급 세부1 스크랩핑
  def scrapCarGradeSubGroup(self):
    #파라조 DB의 모든 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-GRADE-PROCESS =================')
    carDBList = CarGrade.objects.all().select_related().select_related().select_related()
    # print(results)
    crawler = self.crawler

    for grade in carDBList:
      grade_name = grade.name
      modelDetail = grade.modelDetail
      modelDetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      model = modelDetail.model
      brand = model.brand
      print(f"brand: {brand.name}, model: {model.name},  model-detail:{modelDetail_name}, grade_name:{grade_name}")
      # 스크랩 하기
      scrapedResult = crawler.crawlCarGradeSubGroup(brand.name, model.name, modelDetail_name, grade_name)
      if scrapedResult is not None:
        # catg_grade_id = grade.seq
        # carModelDetail = CarModelDetail.objects.get(seq=catg_grade_id)
        # db에 저장하기
        self.storeCarCategoryGradeSubGroup(grade, scrapedResult)
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
    print('END-SCRAPING-CAR-GRADE-PROCESS =================')
    
    return None
  # 카테고리- 등급 스크랩핑
  '''
  차량 카테고리 db에서 모든 리스트를 가져와서 
  하나씩 해당 차량의 등급을 수집해서
  카테고리-등급 테이블에 삽입한다 
  '''
  def scrapCarGrade(self):
    #파라조 DB의 모든 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-GRADE-PROCESS =================')
    carDBList = CarModelDetail.objects.all().select_related().select_related()
    # print(results)
    crawler = self.crawler

    for modelDetail in carDBList:
      modelDetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      catg_modeldetail_id = modelDetail.seq
      model = modelDetail.model
      brand = model.brand
      print(f"brand: {brand.name}, model: {model.name},  model-detail:{modelDetail_name}")
      #스크랩 하기
      scrapedResult = crawler.crawlCarGrade(brand.name, model.name, modelDetail_name)
      if scrapedResult is not None:
        carModelDetail = CarModelDetail.objects.get(seq=catg_modeldetail_id)
        self.storeCarCategoryGrade(carModelDetail, scrapedResult)
      # print(result)
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
    print('END-SCRAPING-CAR-GRADE-PROCESS =================')
    
    return None

  # 차량 카테고리-등급-세부등급1 테이블에 저장
  def storeCarCategoryGradeSubGroup(self, grade, scrapedResult):
    for item in scrapedResult:
      carGradeSubGroup = CarGradeSubGroup(name=item.name, grade=grade)
      carGradeSubGroup.save()

  # 차량 카테고리-등급DB에 저장
  def storeCarCategoryGrade(self, carModelDetail, scrapedResult):
    for item in scrapedResult:
      carGrade = CarGrade(name=item.name, modelDetail=carModelDetail)
      carGrade.save()


  # 차정보 스크래핑
  '''
  차량 카테고리 db에서 모든 리스트를 가져와서 
  하나씩 가격정보를 수집해서
  carinfo 테이블에 삽입한다
  '''
  def scrapCarPrice(self):
    #파라조 DB의 모든 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-PROCESS =================')
    carDBList = CarGrade.objects.all().select_related().select_related().select_related()
    # print(results)
    crawler = self.crawler
    
    for grade in carDBList:
      modelDetail = grade.modelDetail
      model = modelDetail.model
      brand = model.brand
      brand_name = brand.name
      model_name = model.name
      grade_name = grade.name
      modeldetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      
      print(f"brand: {brand_name}, model: {model_name},  model-detail:{modeldetail_name} ")
      
      #스크랩하기
      scrapedResult = crawler.crawlCarPrice(brand_name, model_name, modeldetail_name, grade_name)
      if scrapedResult is not None:
        grade_seq = grade.seq
        modeldetail_seq = modelDetail.seq
        self.storeCarPrice(modeldetail_seq, grade_seq, modeldetail_name, grade_name , scrapedResult)
      # print(result)
    print('END-SCRAPING-CAR-PROCESS =================')
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
  
  # 차량 가격정보 테이블에 저장
  def storeCarPrice(self, modeldetail_id, grade_id, modeldetail_name, grade_name, scrapedResult):
    for item in scrapedResult:
      carinfo = CarInfo(catg_modeldetail_id=modeldetail_id, catg_grade_id=grade_id,  catg_modeldetail_name=modeldetail_name, catg_grade_name=grade_name, carId=item.carId, info=item.info, price=item.price, accident=item.accident, site=item.site)
      carinfo.save()



