import requests
import time
import re
from .Content import Content, CarGrade
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

class CrawlerEncar:

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # UserAgent값을 바꿔줍시다!
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        self.driver = webdriver.Chrome(
            executable_path='C:\work\chromedriver\chromedriver',
            options=chrome_options)
        # driver.implicitly_wait(3)

    def getPageWithSelenium(self, url):
        driver = self.driver
        try:
            self.driver.get(url)
            time.sleep(3)
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tbody#sr_normal > tr')))
            # print(element.text)
            #driver = self.driver  
        except UnexpectedAlertPresentException as e:
            print('[!] Error: ' + str(e))
        except TimeoutException as e:
            print ("Timed out waiting for page to load")
        except Exception as e:
            print("알수업는 예외 발생"+e)
        finally:
            return driver

    def getPageWithSeleniumForCarGrade(self, url):
        driver = self.driver
        try:
            self.driver.get(url)
            time.sleep(2)
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#stepGardeSet')))
            #print('element확인: '+element.text)
        except UnexpectedAlertPresentException as e:
            print('[!] Error: ' + str(e))
        except TimeoutException as e:
            print ("Timed out waiting for page to load")
        except Exception as e:
            print("알수업는 예외 발생"+e)
        finally:
            return driver
         
    def getPageWithBs4(self, url):
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        try:
            req = session.get(url, headers=headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def getDriver(self):
        return self.driver
    
    # 자동차 등급 긁어오기
    def crawlCarGrade(self, company, model, modelDetail):
        # 국내차/수입차에따라 URL 구분
        url = ''
        if self.isDomestic(company) is True:
            url = f'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
        else:
            url = f'http://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
        
        print(url)
        # 셀레니움에 url 요청
       
        driver = self.getPageWithSeleniumForCarGrade(url)
        
        # 컨텐츠 파싱 
        if driver is not None:
            contentList = list() #컨텐트 반환리스트
            selector = '//div[@id="stepGardeSet"]/dl/dd'
            selectedElems = driver.find_elements_by_xpath(selector)
            print('찾은 리스트 개수: '+str(len(selectedElems)))
            if(len(selectedElems) >0):
                for elem in selectedElems:
                    # 등급 이름 
                    name_text = elem.find_element_by_css_selector('label').text
                    print('등급명: '+name_text)
                    # 리스트에 삽입
                    content = CarGrade(name_text)
                    contentList.append(content)
                # pp(contentList)
                return contentList # 컨텐츠 리스트 반환
            
        #url 요청후 컨텐츠가없으면 none
        return None 

    # 자동차 가격정보 긁어오기
    def crawlCarPrice(self, company, model, modelDetail):
        # 국내차/수입차에따라 URL 구분
        url = ''
        if self.isDomestic(company) is True:
            url = f'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
        else:
            url = f'http://www.encar.com/fc/fc_carsearchlist.do?carType=for#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22%7D'
        
        print(url)
        # 셀레니움에 url 요청
        driver = self.getPageWithSelenium(url)
        
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
                    model_text = elem.find_element_by_css_selector('td.inf a').text
                    detail_text = elem.find_element_by_css_selector('td.inf .detail').text
                    info = model_text+detail_text
                    price = elem.find_element_by_css_selector('td.prc_hs').text
                    # accident = self.getCarAccident(carId)
                    # 리스트에 삽입
                    content = Content(carId, '엔카', info, price, accident='미정') 
                    contentList.append(content)
                # pp(contentList)
                return contentList # 컨텐츠 리스트 반환

        #url 요청후 컨텐츠가없으면 none
        return None 

    # 차량 사고이력을 가져오는 함수
    def getCarAccident(self, carId):
        car_detail_url = 'http://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid='+str(carId)
        #차량 상세정보 url
        carAccident = None #사고이력 값
        try:
            carStatePage = self.crawler.getPageWithBs4(car_detail_url)
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
    def obj_dict(self, obj):
        return obj.__dict__

    # 제조사명으로 국내차/수입차 구분
    def isDomestic(self, campany):
        domestic = ['현대','제네시스','기아','쉐보레(GM대우)','르노삼성','쌍용']
        if campany in domestic:
            return True
        return False