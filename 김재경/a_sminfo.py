import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import time

class CompanyCrawler:
    def __init__(self, data_file, driver_options=None):
        self.data_file = data_file
        self.data = pd.read_csv(data_file) 
        self.driver_options = driver_options or self._default_options()
        self.driver = webdriver.Chrome(options=self.driver_options)
        self.sm_res = pd.DataFrame(columns=['기업명', '설립연도', '주소', '매출액', '기업 홈페이지 URL', '업종분류'])
        self.data_1 = self._prepare_data()

    def _default_options(self):
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        return options

    def _prepare_data(self):
        test_list = [zxc[5:8].strip() if isinstance(zxc, str) else zxc for zxc in self.data['주소']]
        data_1 = pd.DataFrame({'기업명': self.data['기업명'], '주소': test_list})
        return data_1.drop_duplicates(subset=['기업명'])

    def _prepare_data(self):
        corp_list = self.data['기업명']
        test_list = [zxc[5:8].strip() if isinstance(zxc, str) else zxc for zxc in self.data['주소']]
        data_1 = pd.DataFrame({'기업명': corp_list, '주소': test_list})
        return data_1.drop_duplicates(subset=['기업명'])

    def login(self, url, username, password):
        self.driver.get(url)
        time.sleep(1)
        first_window_handle = self.driver.window_handles[0]
        self.driver.switch_to.window(first_window_handle)
        time.sleep(1)
        self.driver.find_element(By.ID, "login_id").send_keys(username)
        time.sleep(1)
        self.driver.find_element(By.ID, "login_password").send_keys(password)
        time.sleep(1)
        self.driver.find_element(By.ID, "login_password").send_keys(Keys.ENTER)
        time.sleep(3)

    def navigate_to_company_info(self):
        self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div/ul/li[1]/a').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div/ul/li[1]/ul/li[1]/a').click()
        time.sleep(2)

    def search_company(self, corp_name, address_name):
        self.driver.find_element(By.ID, "searchTxt").clear()
        self.driver.find_element(By.ID, "searchTxt").send_keys(corp_name)
        self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/form[4]/div/div[4]/button[1]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '/html/body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        
        for cat_list in range(1, 11):
            try:
                if corp_name in self.driver.find_element(By.XPATH, f'//*[@id="contents_sub"]/div[3]/form[4]/div/div[7]/table/tbody/tr[{cat_list}]/td[1]/a').text and \
                   address_name in self.driver.find_element(By.XPATH, f'//*[@id="contents_sub"]/div[3]/form[4]/div/div[7]/table/tbody/tr[{cat_list}]/td[5]').text:
                    self.driver.find_element(By.XPATH, f'//*[@id="contents_sub"]/div[3]/form[4]/div/div[7]/table/tbody/tr[{cat_list}]/td[1]/a').click()
                    return True
            except:
                pass
        return False

    def scrape_company_info(self, corp_name):
        time.sleep(3)
        try:
            corp_year = int(''.join(re.findall('\\d\\d\\d\\d', self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/div/table/tbody/tr[2]/td[2]').text)))
        except:
            corp_year = None
        try:
            address = ' '.join(re.findall(r'\b(\w+[구시도남군])\b', self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/div/table/tbody/tr[4]/td').text))
        except:
            address = None
        try:
            sales = int(int(self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/div/div[5]/table/tbody/tr[1]/td[5]').text.replace(',', '')) / 10)
        except:
            sales = None        
        try:
            corp_URL = self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/div/table/tbody/tr[5]/td[1]/a').text
        except:
            corp_URL = None        
        try:
            job_dis = self.driver.find_element(By.XPATH, '//*[@id="contents_sub"]/div[3]/div/table/tbody/tr[6]/td[1]').text
        except:
            job_dis = None        
        
        sm_temp = pd.DataFrame([[corp_name, corp_year, address, sales, corp_URL, job_dis]], 
                               columns=['기업명', '설립연도', '주소', '매출액', '기업 홈페이지 URL', '업종분류'])
        self.sm_res = pd.concat([self.sm_res, sm_temp])

    def crawl(self):
        for corp_name, address_name in zip(self.data_1['기업명'], self.data_1['주소']):
            try:
                self.navigate_to_company_info()
                if self.search_company(corp_name, address_name):
                    self.scrape_company_info(corp_name)
                    time.sleep(3)
                    self.driver.back()
                    time.sleep(57) 
            except Exception as ex:
                print(f"Error processing {corp_name}: {ex}")
                pass

    def save_results(self, file_name):
        self.sm_res.to_csv(file_name, index=False)
