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

    # 셀레니움 초기화 
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # UserAgent값을 바꿔줍시다!
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(
            executable_path='C:\work\chromedriver\chromedriver',
            options=chrome_options)
    
    # 가격정보 가져오기 전용 실레니움 url요청
    def getPageWithSeleniumForCarPrice(self, url):
        driver = None
        try:
            self.driver.get(url)
            time.sleep(2)
            element = WebDriverWait(self.driver, 7).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tbody#sr_normal > tr')))
            # print(element.text)
            driver = self.driver  
        except UnexpectedAlertPresentException as e:
            print('[!] Error: ' + str(e))
        except TimeoutException as e:
            print ("Timed out waiting for page to load")
        except Exception as e:
            print("알수업는 예외 발생"+e)
        finally:
            return driver

    # 등급 가져오기 전용 실레니움 url요청
    def getPageWithSeleniumForCarGrade(self, url):
        driver = None
        try:
            self.driver.get(url)
            time.sleep(2)
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#stepGardeSet')))
            driver = self.driver
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

    # 외부에서 셀레니움 드라이버 참조
    def getDriver(self):
        return self.driver
    
    # 자동차 등급 긁어오기
    def crawlCarGrade(self, company, model, modelDetail):
        # 셀레니움에 url 요청
        url = self.makeUrl(company, model, modelDetail)
        print(url)
       
        driver = self.getPageWithSeleniumForCarGrade(url)
        # URL 요청후 컨텐츠가 있으면 컨텐츠 파싱 
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
            
        # URL 요청후 컨텐츠가 없다면 None리턴
        return None 

    # 자동차 가격정보 긁어오기
    def crawlCarPrice(self, company, model, modelDetail, grade):
        # 셀레니움에 url 요청
        url = self.makeUrl(company, model, modelDetail, grade, 100)
        print('url: '+url)
        driver = self.getPageWithSeleniumForCarPrice(url)
        
        # 컨텐츠 파싱 
        if driver is not None:
            contentList = list() #컨텐트 반환리스트
            selector = '//tbody[@id="sr_normal"]/tr[@data-index]'
            selectedElems = driver.find_elements_by_xpath(selector)
            print('찾은 리스트 개수: '+str(len(selectedElems)))
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
                    accident = self.getCarAccident(carId) #사고이력 조회(새창)
                    # 리스트에 삽입
                    content = Content(carId, '엔카', info, price, accident) 
                    contentList.append(content)
                # pp(contentList)
                return contentList # 컨텐츠 리스트 반환

        #url 요청후 컨텐츠가없으면 none
        return None 

    # 차량 사고이력을 수집함
    def getCarAccident(self, carId):
        print(str(carId)+' 사고이력 조회중..')
        car_detail_url = 'http://www.encar.com/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid='+str(carId)
        #차량 상세정보 url
        carAccident = '미조회' #사고이력 기본 값
        try:
            carStatePage = self.getPageWithBs4(car_detail_url)
            if carStatePage is not None and len(carStatePage) > 0:
                carState = carStatePage.find('table',{'class':'tbl_repair'}).find_all('th')
                for elm in carState:
                    if('사고이력' in elm.get_text()):
                        carAccident = elm.find_next_siblings("td")[0].find('span', class_="on").get_text()
                        break
        except AttributeError as e:
            print('사고이력 조회 에러')
        finally:
            return carAccident

    # 딕셔너리를 json 객체로 변환시켜주는 함수
    def obj_dict(self, obj):
        return obj.__dict__

    # 제조사명으로 국내차/수입차 구분
    def isDomestic(self, campany):
        domestic = ['현대','제네시스','기아','쉐보레(GM대우)','르노삼성','쌍용']
        if campany in domestic:
            return True
        return False

    # 엔카 param  다시쓰기
    def adjustParam(self, text):
        #엔카에서는 .(점)앞에 언더바를 붙이는 규칙이 있음
        return text.replace('.','_.')
        
    # 엔카 url 만들기
    def makeUrl(self, company, model, modelDetail, grade, limit):
        url = ''
        pre = ''
        tail = ''
        cartype= ''
        # url = f"http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22{limit}%7D"
        if limit is not None:
            limit ="%2C%22limit%22%3A%22"+str(limit)+"%22"

        if self.isDomestic(company) is True:
            pre = 'dc/dc_carsearchlist.do?carType=kor'
        else:
            pre = 'fc/fc_carsearchlist.do?carType=for'
        
        if grade is not None:
            tail = f"_.(C.Model.{modelDetail}._.BadgeGroup.{grade}.)))))%22{limit}%7D"
            cartype='CarType.Y'
        else:
            tail = f"_.Model.{modelDetail}.))))%22{limit}%7D"
            cartype='CarType.N'
    
        model = self.adjustParam(model)
        modelDetail = self.adjustParam(modelDetail)
        url = f"http://www.encar.com/{pre}#!%7B%22action%22%3A%22(And.Hidden.N._.(C.{cartype}._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}."+tail
        
        return url
