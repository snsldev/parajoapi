from .crawler import Crawler

def searchFromEncar(company, model, modelDetail):
  # company = company
  # model = model 
  # modelDetail = modelDetail
  url = f'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
  crawl = Crawler()
  driver = crawl.getPageWithSelenium(url)
  if driver is not None:
    # contentList = list()
    selector = '//tbody[@id="sr_normal"]/tr[@data-index]'
    selectedElems = driver.find_elements_by_xpath(selector)
    if(len(selectedElems) >0):
      # print(len(selectedElems))
      for elem in selectedElems:
        print(elem.text)
        modelDetail = elem.find_element_by_css_selector('td.inf').text
        price = elem.find_element_by_css_selector('td.prc_hs').text
        carAccident = getCarState(elem, crawl)
        content = Content(carid, modelDetail, price, carState)   
        contentList.append(content)
    
      driver.close()
  # return contentList 

  # print(url)
  return {
        'message' : '안녕 파이썬 장고',
        'items' : ['파이썬', '장고', 'AWS', 'Azure'],
  }

  def getCarState(carItem, crawler):
    #차량 고유 id 찾기
    link = carItem.find_element_by_css_selector('a').get_attribute('href')
    regex = re.compile("(carid=)(([0-9]?)+)")
    matchobj = regex.search(link)
    carid = matchobj.group(2) 

    car_detail_url = 'http://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid='+str(carid)#차량 상세정보 url
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