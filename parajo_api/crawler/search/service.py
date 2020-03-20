from .crawler import Crawler
import re
from pprint import pprint as pp
from .content import Content

def searchFromEncar(company, model, modelDetail):
  url = f'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
  crawl = Crawler()
  driver = crawl.getPageWithSelenium(url)

  if driver is not None:
    contentList = list() #컨텐트 반환리스트 
    selector = '//tbody[@id="sr_normal"]/tr[@data-index]'
    selectedElems = driver.find_elements_by_xpath(selector)
    if(len(selectedElems) >0):
      # print(len(selectedElems))
      for elem in selectedElems:
        #차량 고유 id
        link = elem.find_element_by_css_selector('a').get_attribute('href')
        regex = re.compile("(carid=)(([0-9]?)+)")
        matchobj = regex.search(link)
        carId = matchobj.group(2) 
        # print('carId'+carId)

        info = elem.find_element_by_css_selector('td.inf').text
        price = elem.find_element_by_css_selector('td.prc_hs').text
        accident = getCarAccident(carId, crawl)
        
        content = Content(carId, '엔카', info, price, accident) # 컨텐트 객체 생성
        contentList.append(obj_dict(content)) # 리스트에 넣기
    # pp(contentList)
    driver.close()
    return contentList
  return None

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

def obj_dict(obj):
    return obj.__dict__