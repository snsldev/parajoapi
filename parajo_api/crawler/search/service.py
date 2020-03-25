from .crawler import Crawler
import re
from pprint import pprint as pp
from .content import Content

def searchFromEncar(company, model, modelDetail):
  # 국내차/수입차에따라 URL 구분
  url = ''
  if isDomestic(company) is True:
   url = f'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
  else:
   url = f'http://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
 
  # print(url)
  # 셀레니움 초기화 및 웹드라이버에 url 요청
  crawl = Crawler()
  driver = crawl.getPageWithSelenium(url)
  
  # 컨텐츠 파싱 
  if driver is not None:
    contentList = list() #컨텐트 반환리스트
    selector = '//tbody[@id="sr_normal"]/tr[@data-index]'
    selectedElems = driver.find_elements_by_xpath(selector)
    # print('len:'+str(len(selectedElems)))
    if(len(selectedElems) >0):
      for elem in selectedElems:
        #차량 고유 id
        link = elem.find_element_by_css_selector('a').get_attribute('href')
        # print('link:'+link)
        regex = re.compile("(carid=)(([0-9]?)+)")
        matchobj = regex.search(link)
        carId = matchobj.group(2) 
        # print('carId:'+carId)
        # 차량 정보
        info = elem.find_element_by_css_selector('td.inf').text
        price = elem.find_element_by_css_selector('td.prc_hs').text
        # accident = getCarAccident(carId, crawl)
        # json으로 변환후 리스트에 삽입
        content = Content(carId, '엔카', info, price, accident=None) 
        contentList.append(obj_dict(content)) 
    # pp(contentList)
    driver.close() 
    return contentList # 컨텐츠 리스트 반환

  #url 요청후 컨텐츠가없으면 none
  return None 

# 차량 사고이력을 가져오는 함수
def getCarAccident(carId, crawler):
    car_detail_url = 'http://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid='+str(carId)
    #차량 상세정보 url
    carAccident = None #사고이력 값
    try:
      carStatePage = crawler.getPageWithBs4(car_detail_url)
      if carStatePage is not None and len(carStatePage) > 0:
        carState = carStatePage.find('table',{'class':'tbl_repair'}).find_all('th')
        for elm in carState:
          if('사고이력' in elm.get_text()):
            carAccident = elm.find_next_siblings("td")[0].find('span', class_="on").get_text()
            break
      return carAccident
    except AttributeError as e:
      return None

# 딕셔너리를 json 객체로 변환시켜주는 함수
def obj_dict(obj):
    return obj.__dict__

# 제조사명으로 국내차/수입차 구분
def isDomestic(campany):
  domestic = ['현대','제네시스','기아','쉐보레(GM대우)','르노삼성','쌍용']
  if campany in domestic:
    return True
  return False