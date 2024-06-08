from a_sminfo import CompanyCrawler
from a_wanted import wanted_crawling_program
import pandas as pd
from dotenv import load_dotenv
import os
import re

load_dotenv()
print(os.getenv('userid'))
print(os.getenv('password'))

def crawler():

    # wanted_res = wanted_crawling_program(1, 5)
    # wanted_res.기업명 = wanted_res.기업명.apply(lambda x: re.sub(r'\([^)]*\)','',x))
    # wanted_res.기업명 = wanted_res.기업명.apply(lambda x: re.sub('\\W', '', x))

    # wanted_res.to_csv("wanted_res.csv", index = False)

    url = 'https://sminfo.mss.go.kr/cm/sv/CSV001R0.do'
    username = os.getenv('userid')
    password = os.getenv('password')

    # 데이터 파일 경로
    data_file = 'wanted_res.csv'
    output_file = 'company_info.csv'

    # 크롤러 객체 생성
    crawler = CompanyCrawler(data_file)
    
    # 로그인
    crawler.login(url, username, password)
    
    # 크롤링 수행
    crawler.crawl()
    
    # 결과 저장
    crawler.save_results(output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    crawler()