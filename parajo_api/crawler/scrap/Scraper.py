from ..models import CarModelDetail, CarInfo, CarGrade, CarGradeSubGroup, CarGradeSub
from .CrawlerEncar import CrawlerEncar
import re

'''
스크랩퍼는 정형화 된 데이터를 본사DB에 저장하는 역할을 수행
'''
class Scrapper:

  def __init__(self, crawler: CrawlerEncar):
    self.crawler = crawler

  # 카테고리 - 세부등급2 스크랩
  def scrapCarGradeSub(self):

    #파라조 차량 카테고리(브랜드-모델-세부모델-등급-세부등급1) 리스트를 불러옴
    print('START-SCRAPING-CAR-GRADE-SUB-PROCESS =================')
    carDBList = CarGradeSubGroup.objects.all().select_related().select_related().select_related().select_related()
    # print(results)
    crawler = self.crawler

    for gradeSubGroup in carDBList:
     
      grade = gradeSubGroup.grade # 등급
      grade_name = grade.name 
      modelDetail = grade.modelDetail # 세부모델
      modelDetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      #modelDetail_name = modelDetail.name.strip()
      model = modelDetail.model
      brand = model.brand
      grade_subgroup_name = gradeSubGroup.name
     
      print(f"brand: {brand.name}, model: {model.name},  model-detail:{modelDetail_name}, grade_name:{grade_name}, grade_subgroup_name:{grade_subgroup_name}")
     
      # 스크랩 하기
      scrapedResult = crawler.crawlCarGradeSub(brand.name, model.name, modelDetail_name, grade_name, grade_subgroup_name)
      if scrapedResult is not None:
        # db에 저장하기
        self.storeCarCategoryGradeSub(gradeSubGroup, scrapedResult)
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
    print('END-SCRAPING-CAR-GRADE-SUB-PROCESS =================')

  # 카테고리 - 세부등급1 스크랩
  def scrapCarGradeSubGroup(self):
    #파라조 DB의 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-GRADE-SUBGROUP-PROCESS =================')
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
    print('END-SCRAPING-CAR-GRADE-SUBGROUP-PROCESS =================')
    
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

  # 차량 카테고리-등급-세부등급2 테이블에 저장
  def storeCarCategoryGradeSub(self, gradeSubGroup, scrapedResult):
    for item in scrapedResult:
      carGradeSub = CarGradeSub(name=item.name, gradeSubGroup=gradeSubGroup)
      carGradeSub.save()

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


  # 차량 가격정보를 스크래핑
  '''
  차량 카테고리 DB의 등급테이블까지 조인한 레코드를 가져와서 
  하나씩 가격정보를 수집해서
  carinfo 테이블에 삽입한다
  '''
  def scrapCarPrice(self):
    #파라조 DB의 모든 차량 카테고리 리스트를 불러옴
    print('START-SCRAPING-CAR-PROCESS =================')
    # carDBList = ''
    # carDBList = CarGradeSubGroup.objects.all().select_related().select_related().select_related().select_related()
    carDBList = CarGradeSubGroup.objects.all().prefetch_related('cargradesubs').select_related().select_related().select_related().select_related()
    # if gradeSub is not None:
    #   # 세부등급2가 존재하면 세부등급2까지 조인
    #   carDBList = CarGradeSubGroup.objects.all().select_related().select_related().select_related().select_related()
    # elif gradeSubGroup is not None:
    #   # 세부등급1이 존재하면 세부등급1까지 조인
    #   carDBList = CarGradeSub.objects.all().select_related().select_related().select_related().select_related().select_related()
    # else:
    #   # 세부등급1이 존재하면
    #   carDBList = CarGrade.objects.all().select_related().select_related().select_related()


    # print(results)
    crawler = self.crawler
    # cnt=0
    # 이전 모델명을 저장하기위한 변수
    #prev_modelDetail_name = None;
    prev_modelDetail_seq = None;
    prev_grade_seq = None;

    for gradeSubGroup in carDBList:
      gradeSubList = gradeSubGroup.cargradesubs.all()
      grade_sub_group_name = gradeSubGroup.name
      grade = gradeSubGroup.grade
      modelDetail = grade.modelDetail
      model = modelDetail.model
      brand = model.brand
      # if brand.region == 'domestic':
      #   continue
      brand_name = brand.name
      model_name = model.name
      if brand.checked ==1 : 
        continue
      if model.checked ==1 : 
        continue
      if modelDetail.checked ==1 : 
        continue
      if grade.checked ==1 : 
        continue

      modeldetail_name = re.sub('\(([^\)])*~(.)*\)', '', modelDetail.name).strip() # (~년식정보) 제거후 앞뒤 공백 제거
      grade_name = grade.name
      modeldetail_seq = modelDetail.seq
      grade_seq = grade.seq
      grade_subgroup_seq = gradeSubGroup.seq

       # modelDetail 한단위를 다 저장하면 체크됨으로 업데이트
      if (prev_modelDetail_seq is not None) and (prev_modelDetail_seq != modeldetail_seq): 
         CarModelDetail.objects.filter(seq=prev_modelDetail_seq).update(checked=1)
       # grade 한단위를 다 저장하면 체크됨으로 업데이트
      if (prev_grade_seq is not None) and (prev_grade_seq != grade_seq): 
         CarModelDetail.objects.filter(seq=grade_seq).update(checked=1)
    
      if gradeSubList.count() == 0:
        # 카테고리에 세부등급2가 없을때
        # 세부등급1까지 가격 가져옴
        print(f"브랜드: {brand_name}, 모델: {model_name},  상세모델:{modeldetail_name}, 등급:{grade_name}, 세부등급1:{grade_sub_group_name} ")
        # cnt+=1
        scrapedResult = crawler.crawlCarPrice(brand_name, model_name, modeldetail_name, grade_name, grade_sub_group_name, None)
        if scrapedResult is not None:
          self.storeCarPrice(modeldetail_seq, grade_seq, grade_subgroup_seq, None, brand_name, model_name, modeldetail_name, grade_name, grade_sub_group_name, None, scrapedResult)
      else:
        for gradeSub in gradeSubList:
          grade_sub_name = gradeSub.name
          grade_sub_seq = gradeSub.seq
          print(f"브랜드: {brand_name}, 모델: {model_name},  상세모델:{modeldetail_name}, 등급:{grade_name}, 세부등급1:{grade_sub_group_name}, 세부등급2:{grade_sub_name} ")
          # cnt+=1
          #스크랩하기
          scrapedResult = crawler.crawlCarPrice(brand_name, model_name, modeldetail_name, grade_name, grade_sub_group_name, grade_sub_name)
          if scrapedResult is not None:
             self.storeCarPrice(modeldetail_seq, grade_seq, grade_subgroup_seq, grade_sub_seq, brand_name, model_name, modeldetail_name, grade_name, grade_sub_group_name, grade_sub_name, scrapedResult)
     
      # 저장완료하면 이름과 시퀀스를 임시로 갖고있는다
      # prev_modelDetail_name = modeldetail_name
      prev_modelDetail_seq = modeldetail_seq
      prev_modelDetail_seq = grade_seq


    # print('all count is :'+str(cnt))
    print('END-SCRAPING-CAR-PROCESS =================')
    crawler.getDriver().quit() #끝났으면 셀레니움 브라우져 정상종료
  
  # 차량 가격정보 테이블에 저장
  def storeCarPrice(self, modeldetail_id, grade_id, grade_subgroup_id, grade_sub_id, brand_name, model_name, modeldetail_name, grade_name, grade_subgroup_name, grade_sub_name, scrapedResult):
    for item in scrapedResult:
      carinfo = CarInfo(
        catg_modeldetail_id=modeldetail_id,
        catg_grade_id=grade_id, 
        catg_grade_subgroup_id= grade_subgroup_id,
        catg_grade_sub_id= grade_sub_id,
        catg_brand_name=brand_name, 
        catg_model_name=model_name, 
        catg_modeldetail_name=modeldetail_name, 
        catg_grade_name=grade_name, 
        catg_grade_subgroup_name=grade_subgroup_name, 
        catg_grade_sub_name=grade_sub_name, 
        carId=item.carId, 
        init_regdate_year=item.init_regdate_year, 
        init_regdate_month=item.init_regdate_month, 
        distance=item.distance, 
        price=item.price, accident=item.accident, site=item.site )

      #같은 상품아이디 존재하면 하지 않음
      exist_carid_cnt = CarInfo.objects.filter(carId=carinfo.carId).count() 
      if exist_carid_cnt > 0:
        print("중복데이터 입니다 record insert pass!, carId is: "+carinfo.carId)
        continue

      carinfo.save()



