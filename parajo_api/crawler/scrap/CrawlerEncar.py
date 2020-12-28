import requests
import time
import re
from .Content import Content, CarGrade, CarGradeSubGroup, CarGradeSub
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib.parse import quote, urlencode
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

class CrawlerEncar:
 
    # 셀레니움 초기화 
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # UserAgent값 변경시
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        chromedriver_path=os.path.join(PROJECT_PATH, 'chromedriver/chromedriver')

        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path,
            options=chrome_options)



    # 실레니움 url요청
    def getPageWithSelenium(self, url, mode):

        driver = self.driver
        try:
            driver.get(url)
            if mode == 'price':
                # time.sleep(5)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tbody#sr_normal > tr')))
            elif mode == 'modeldetail':
                time.sleep(2)
                element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#stepGardeSet')))
            elif mode == 'grade':
                time.sleep(2)
                element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'dl#stepGared_0')))
            elif mode == 'gradeSubGroup':
                print('==driver url mode is gradeSubGroup')
                time.sleep(2)
                element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'dl#stepDeGared'))) #수정됨
            
        except UnexpectedAlertPresentException as e:
            print('[!] Error: ' + str(e))
            return None
        except TimeoutException as e:
            print ("Timed out waiting for page to load")
            return None
        except Exception as e:
            print("알수업는 예외 발생"+e)
            return None
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
    
    # 카테고리 세부등급2 크롤링
    def crawlCarGradeSub(self, company, model, modelDetail, grade, gradeSubGroup):
        print("===call crawlCarGradeSub")
        # 셀레니움에 url 요청
        url = self.makeUrlUnderGrade(company, model, modelDetail, grade, gradeSubGroup, None, None)
        print(url)
        
        #세부등급1을 요청해야 세부등급2가 나옴    
        driver = self.getPageWithSelenium(url, 'gradeSubGroup')

        # URL 요청후 컨텐츠가 있으면 컨텐츠 파싱 
        if driver is not None:
            contentList = list() #컨텐트 반환리스트
            selector = '//dl[@id="stepDeGared"]/dd/p' #수정됨
            selectedElems = driver.find_elements_by_xpath(selector)
            print('찾은 리스트 개수: '+str(len(selectedElems)))
            if(len(selectedElems) > 0):
                for elem in selectedElems:
                    # 세부등급2 이름 
                    name = elem.find_element_by_css_selector('label').get_attribute('title') #수정됨
                    print('세부등급2 명: '+name)
                    # 리스트에 삽입
                    content = CarGradeSub(name)
                    contentList.append(content)
        
                return contentList # 컨텐츠 리스트 반환
            
        # URL 요청후 컨텐츠가 없다면 None리턴
        return None 

    # 카테고리 세부등급1 크롤링
    def crawlCarGradeSubGroup(self, company, model, modelDetail, grade):
        # 셀레니움에 url 요청
        url = self.makeUrlUnderGrade(company, model, modelDetail, grade, None, None, None)
        print(url)
       
        driver = self.getPageWithSelenium(url, 'grade')
        # URL 요청후 컨텐츠가 있으면 컨텐츠 파싱 
        if driver is not None:
            contentList = list() #컨텐트 반환리스트
            selector = '//dl[@id="stepGared_0"]/dd/p'
            selectedElems = driver.find_elements_by_xpath(selector)
            print('찾은 리스트 개수: '+str(len(selectedElems)))
            if(len(selectedElems) > 0):
                for elem in selectedElems:
                    # 세부등급1 이름 
                    name = elem.find_element_by_css_selector('label').get_attribute('title')
                    print('세부등급1 명: '+name)
                    # 리스트에 삽입
                    content = CarGradeSubGroup(name)
                    contentList.append(content)
                    
                # pp(contentList)
                return contentList # 컨텐츠 리스트 반환
            
        # URL 요청후 컨텐츠가 없다면 None리턴
        return None 

    # 카테고리-등급 크롤링
    def crawlCarGrade(self, company, model, modelDetail):
        # 셀레니움에 url 요청
        url = self.makeUrl(company, model, modelDetail)
        print(url)
       
        driver = self.getPageWithSelenium(url, 'modeldetail')
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

    # 차량가격정보 크롤링
    def crawlCarPrice(self, company, model, modelDetail, grade, gradeSubGroup, gradeSub):
        # 셀레니움에 url 요청
        url = self.makeUrlUnderGrade(company, model, modelDetail, grade, gradeSubGroup, gradeSub, 50)
        print('url: '+url)
        driver = self.getPageWithSelenium(url, 'price')
        
        # 컨텐츠 파싱 
        if driver is not None:
            contentList = list() #컨텐트 반환리스트
            selector = '//tbody[@id="sr_normal"]/tr[@data-index]'
            selectedElems = driver.find_elements_by_xpath(selector)
            print('찾은 목록 개수 : '+str(len(selectedElems)))
            if(len(selectedElems) >0):
                for elem in selectedElems:
                    
                    # print('getcssvalue: '+str(elem.value_of_css_property("display")))
                    if elem.value_of_css_property("display") == 'none': 
                        continue

                    #차량 고유 id
                    link = elem.find_element_by_css_selector('a').get_attribute('href')
                    # print('link:'+link)
                    regex = re.compile("(carid=)(([0-9]?)+)")
                    matchobj = regex.search(link)
                    carId = matchobj.group(2) 
                    print('carId:'+carId)
                    # 차량 정보
                    model_text = elem.find_element_by_css_selector('td.inf a').text
                    detail_text = elem.find_element_by_css_selector('td.inf .detail').text
                    #최초등록 년,월 분리
                    yymm_unform = elem.find_element_by_css_selector('td.inf .detail .yer').text
                   # print('yymm_unform: '+str(yymm_unform))
                    yymm_arr = yymm_unform.split('/')
                   # print('yymm_arr: '+str(yymm_arr))
                    init_regdate_year = yymm_arr[0] #년
                    # init_regdate_month = yymm_arr[1][0]+yymm_arr[1][1] #월
                    init_regdate_month = yymm_arr[1].split('식')[0]
                    # 주행거리
                    distance_unform = elem.find_element_by_css_selector('td.inf .detail .km').text
                    distance = distance_unform.replace(',','').replace('km','') 

                    # info = model_text+detail_text
                    # 비정상 가격 데이터는 수집안함
                    try:
                        if elem.find_element_by_css_selector('td.prc_hs .type_leaserent'): 
                            print('리스승계 엘리먼트 건너뜀: '+elem.find_element_by_css_selector('td.prc_hs .type_leaserent').text)
                            continue
                    except :
                        pass            

                    price = elem.find_element_by_css_selector('td.prc_hs strong').text.replace(',','') 
                    
                    # 숫자인지 검사(음의정수도 걸러짐)
                    if not price.isdecimal() :
                        continue
                    
                    # 0인가격 또는 9999인 가격 제외제외
                    if price == '0' or price == '9999':
                        continue

                    # 150이하 가격 제외
                    if int(price) <= 150:
                        continue

                    # accident = self.getCarAccident(carId) #사고이력 조회(새창)
                    # 리스트에 삽입
                    content = Content(carId, '엔카', init_regdate_year, init_regdate_month, distance, price, accident=None) 
                    contentList.append(content)
                ##새탭열기
                driver.execute_script("window.open();")
                windows_after = driver.window_handles[1]
                driver.close()
                driver.switch_to.window(windows_after)
                

                # pp(contentList)
                return contentList # 컨텐츠 리스트 반환
            
        #url 요청후 컨텐츠가없으면 none
        return None 

    # 차량 사고이력 크롤링
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
            cartype='CarType.Y'
        else:
            pre = 'fc/fc_carsearchlist.do?carType=for'
            cartype='CarType.N'
        
        modelDetail = self.adjustParam(modelDetail)
        modelDetail = quote((modelDetail))

        model = self.adjustParam(model)
        model = quote(model)

        if grade is not None:
            tail = f"_.(C.Model.{modelDetail}._.BadgeGroup.{quote(grade)}.)))))%22{limit}%7D"
        else:
            tail = f"_.Model.{modelDetail}.))))%22{limit}%7D"
    
        url = f"http://www.encar.com/{pre}#!%7B%22action%22%3A%22(And.Hidden.N._.(C.{cartype}._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}."+tail
        # print(url)
        return url

    # 엔카 url 만들기
    def makeUrlUnderGrade(self, company, model, modelDetail, grade, gradeSubGroup, gradeSub, limit):
        url = ''
        pre = ''
        tail = ''
        cartype= ''
        # url = f"http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}._.Model.{modelDetail}.))))%22{limit}%7D"
        if limit is not None:
            limit = "%2C%22limit%22%3A%22"+str(limit)+"%22"
        else:
            limit = ''

        if self.isDomestic(company) is True:
            pre = 'dc/dc_carsearchlist.do?carType=kor'
            cartype='CarType.Y'
        else:
            pre = 'fc/fc_carsearchlist.do?carType=for'
            cartype='CarType.N'
        
        model = self.adjustParam(model)
        model = quote(model)
        
        modelDetail = self.adjustParam(modelDetail)
        modelDetail = quote((modelDetail))

        grade = self.adjustParam(grade)
        grade = quote(grade)

        tail = f"_.(C.Model.{modelDetail}._.BadgeGroup.{grade}.)))))%22{limit}%7D"

        if gradeSubGroup is not None:
            # gradeSubGroup url 코드작성
            gradeSubGroup = self.adjustParam(gradeSubGroup)
            gradeSubGroup = quote(gradeSubGroup)
            tail = f"_.(C.Model.{modelDetail}._.(C.BadgeGroup.{grade}._.Badge.{gradeSubGroup}.))))))%22{limit}%7D" 
            
            if gradeSub is not None:
                # gradeSub url 코드작성
                gradeSub = self.adjustParam(gradeSub)
                gradeSub = quote(gradeSub)
                tail = f"_.(C.Model.{modelDetail}._.(C.BadgeGroup.{grade}._.(C.Badge.{gradeSubGroup}._.BadgeDetail.{gradeSub}.)))))))%22{limit}%7D" #수정요

    
        url = f"http://www.encar.com/{pre}#!%7B%22action%22%3A%22(And.Hidden.N._.(C.{cartype}._.(C.Manufacturer.{company}._.(C.ModelGroup.{model}."+tail
        # print(url)
        return url
