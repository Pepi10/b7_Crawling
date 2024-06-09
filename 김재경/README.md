## 데이터 수집 프로젝트
* 목적
  * AWS 교육 서비스를 진행하기 위해 관련 업체의 채용정보를 수집하기 위함
* 프로젝트 설명
  * __AWS_채용공고_김재경.pdf__
* 느낀점
  * Selenium을 사용하여 드라이버를 컨트롤 하는 법에 익숙해졌다.
  * LSD (Latent Semantic Analysis)와 LDA (Latent Dirichlet Allocation), TF-IDF를 통해 키워드 추출하는 법을 공부.
  * 첫 프로젝트라 처리방식과 스케줄링에 어려움을 겪었다. 본인 역량 파악이 중요한 것 같다.

## Libraries

<img src="https://img.shields.io/badge/-Selenium-43B02A?style=flat-square&logo=Selenium&logoColor=white" /> <img src="https://img.shields.io/badge/-BeautifulSoup-181717?style=flat-square&logo=BeautifulSoup&logoColor=white" /> <img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white" /> <img src="https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=Pandas&logoColor=white" /> <img src="https://img.shields.io/badge/-Konlpy-FFD43B?style=flat-square&logo=Python&logoColor=white" /> <img src="https://img.shields.io/badge/-Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" /> <img src="https://img.shields.io/badge/-Matplotlib-11557C?style=flat-square&logo=Matplotlib&logoColor=white" /> <img src="https://img.shields.io/badge/-Seaborn-4E4E4E?style=flat-square&logo=Seaborn&logoColor=white" /> <img src="https://img.shields.io/badge/-Wordcloud-FFA500?style=flat-square&logo=Python&logoColor=white" />

## How to run
---
> .env 설정
```
userid=your sm info ID
password=your sm info Password
```
> Crawling Data

```bash
python crawler.py
```
> Visualization

```bash
streamlit run streamlit.py
```
