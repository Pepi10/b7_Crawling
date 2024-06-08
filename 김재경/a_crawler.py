import pandas as pd
from dotenv import load_dotenv
import os, re

from a_sminfo import CompanyCrawler
from a_wanted import wanted_crawling_program

from a_transform import (run_preprocess_career, 
                         preprocess_address,
                         TextProcessor_1,
                         TextProcessor_2
                         )

load_dotenv()
print(os.getenv('userid'))
print(os.getenv('password'))

def crawler():

#########################################  Wanted  #########################################

    ### 크롤링 ###
    wanted_res = wanted_crawling_program(1, 5)
    wanted_res.기업명 = wanted_res.기업명.apply(lambda x: re.sub(r'\([^)]*\)','',x))
    wanted_res.기업명 = wanted_res.기업명.apply(lambda x: re.sub('\\W', '', x))

    ### 직급, 주소 전처리 ###
    run_preprocess_career(wanted_res)
    preprocess_address(wanted_res)
    wanted_res = wanted_res.reset_index().drop(columns={"index"})
    
    ### 자격요건 LSA ###
    processor = TextProcessor_1()
    X_reduced, top_keywords = processor.process_text_data(wanted_res['자격요건'])

    wanted_res['자격요건_주제'] = X_reduced.argmax(axis=1) + 1
    wanted_res['자격요건_키워드'] = wanted_res['자격요건_주제'].apply(lambda x: ', '.join(sorted(top_keywords[x-1])))

    ### 이용하는기술스택/우대사항 LDA ###
    processor = TextProcessor_2()
    processed_data = processor.process_data(wanted_res)
    processed_data

    ### Wanted DataFrame Load ### 
    processed_data.to_csv("wanted_res.csv", index = False)

######################################### SM info #########################################

    ### CompanyCrawler 인자 ###
    url = 'https://sminfo.mss.go.kr/cm/sv/CSV001R0.do'
    username = os.getenv('userid')
    password = os.getenv('password')
    # 데이터 파일 경로
    data_file = 'wanted_res.csv'
    output_file = 'company_info.csv'

    ### CompanyCrawler ###
    crawler = CompanyCrawler(data_file)
    crawler.login(url, username, password)
    crawler.crawl()
    
    ### SM info DataFrame Load ### 
    crawler.save_results(output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    crawler()