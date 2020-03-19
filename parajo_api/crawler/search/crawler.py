import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

class Crawler:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path='C:\work\chromedriver\chromedriver',
            options=chrome_options)

    def getPageWithSelenium(self, url):
        try:
            self.driver.get(url)
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'sr_normal')))
        except TimeoutException as e:
            print('timeoutException: '+e)
            return None
        return self.driver  
         
    def getPageWithBs4(self, url):
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        try:
            req = session.get(url, headers=headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
        
    def getResult(self, company, model, modelDetail):
        return {
        'company' : company,
        'model' : model,
        'modeldetail' : modelDetail,
    }

