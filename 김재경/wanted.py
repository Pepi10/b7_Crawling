import pandas as pd
import re, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wanted_crawling_program(start_post, end_post):
    """
    이 함수는 공고를 4회 클릭시 로그인창이 발생하는 사이트의 특성 때문에
    try에서 3개의 공고를 클릭하여 크롤링한 후 
    finally에서 driver를 종료시킨 다음 드라이브를 켜 반복을 이어갑니다.
    """

    url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=job.recommend_order&years=-1&locations=all"

    wanted_res = pd.DataFrame(
        columns = ['기업명', '주소', '직무', '자격요건', '직급', '이용하는기술스택/우대사항', '해당 페이지 URL']
        )

    for job in range(2, 36):
        driver = start_driver()
        driver.get(url)

        ### 직무 선택 클릭 ###
        search_job = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="__next"]/div[3]/div[1]/section/div[1]/section/div/button/span/span'
                )))
        search_job.click()        
        job_dis = driver.find_element(
            By.XPATH, f'//*[@id="__next"]/div[3]/div[1]/section/div[1]/section/div/div/div[2]/div[2]/ul[2]/button[{job}]/p'
            ).text
        driver.find_element(
            By.XPATH, f'//*[@id="__next"]/div[3]/div[1]/section/div[1]/section/div/div/div[2]/div[2]/ul[2]/button[{job}]'
            ).click()
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[3]/div[1]/section/div[1]/section/div/div/div[2]/div[3]/button[2]/span[2]'
            ).click()
        
        time.sleep(1.1)
        ### aws 검색하기 ###
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                    By.XPATH, '//*[@id="__next"]/div[3]/div[1]/section/div[2]/ul/button[2]'
                    )))
        search.click()

        time.sleep(1.5)
        for _ in "AWS":
            time.sleep(0.5)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/div[1]/input'
                ))
            ).send_keys(_)
              
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div[2]/div/footer/div/button[2]/span[2]'
            ).click()
        time.sleep(.5)
        start_time_scroll = time.time()
        
        # 크롤링 코드블럭
        try:
            for post_job in range(start_post, end_post):
                if time.time() - start_time_scroll > 60:
                    break 
                ### 스크롤하며 공고 찾기 ###
                while True:
                    try:
                        time.sleep(.5)
                        post = driver.find_element(
                            By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/ul/li[{post_job}]/div/a/div[1]'
                            )
                        time.sleep(0.1)
                        try:
                            if post.is_displayed():
                                post.click()
                                break
                        except:
                            driver.execute_script("window.scrollBy(0, 100);")
                            if post.is_displayed():
                                post.click()
                                break
                    except:
                        driver.execute_script("window.scrollBy(0, 100);")
                        if post.is_displayed():
                            post.click()
                            break

                    # 스크롤 시작점=0, ?픽셀씩 내리기
                    driver.execute_script("window.scrollBy(0, 430);")
                    time.sleep(0.6)

                    if time.time() - start_time_scroll > 60:
                        break  
                # while 코드 끝  
                # while 코드에서 클릭한 공고의 data crawling 코드

                # 공고 클릭 후 Data Crawling
                corp = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                        By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/a'
                        )
                        )
                        ).text
                time.sleep(0.2)
                #더보기 클릭
                driver.find_element(
                    By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button'
                    ).click()
                time.sleep(0.2)
                tec = driver.find_element(
                    By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[3]/p/span'
                    ).text.replace('\n',', ')
                time.sleep(0.2)
                car = driver.find_element(
                    By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[4]'
                    ).text
                time.sleep(0.2)
                post_url = [q.get_attribute('href') for q in driver.find_elements(By.TAG_NAME, 'link')][0]
                time.sleep(0.2)
                main = re.sub(
                    '\s', '', driver.find_element(
                        By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[2]/p/span'
                        ).text
                        ).replace('-', ', ')[1:]
                time.sleep(0.2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                span_tag = soup.find('span', class_='Typography_Typography__root__xYuMs Typography_Typography__body2__EpxWz Typography_Typography__weightMedium__O0Rdi')
                address = span_tag.get_text()
                
                # Data 인덱스 아래부터 concat
                wanted_temp = pd.DataFrame(
                    [corp, address, job_dis, main, car, tec, post_url],
                    index = ['기업명', '주소', '직무', '자격요건', '직급', '이용하는기술스택/우대사항', '해당 페이지 URL']
                    ).T
                wanted_res = pd.concat(
                    [wanted_res, wanted_temp]
                    )
                
                time.sleep(0.3)
                # 뒤로가기
                driver.back()
                time.sleep(0.3)
        except:
            pass


        finally:
            driver.quit()
            time.sleep(.5)
        
    return wanted_res