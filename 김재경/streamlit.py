import streamlit as st
import pandas as pd
from visualization import (sales_distribution,
                           establishment_year,
                           position_years,
                           industry_distribution,
                           address,
                           visualize_wordcloud)

# 데이터 불러오기
data = pd.read_csv('wanted_res.csv')

# Streamlit 앱 시작
st.title("시각화 예시")

## 1. 매출액 구간별 데이터 분포 시각화
st.header("매출액 구간별 데이터 분포")
sales_distribution(data)

## 2. 설립연도 데이터 분포 시각화
st.header("설립연도 데이터 분포")
establishment_year(data)

## 3. 직급(연차)별 데이터 분포 시각화
st.header("직급(연차)별 데이터 분포")
position_years(data)

## 4. 업종분류의 비율 시각화
st.header("업종분류의 비율")
industry_distribution(data)

## 5. 기업 주소 시각화
st.header("기업 주소 시각화")
address(data)

## 6. 자격요건 및 우대사항 워드클라우드 시각화
st.header("자격요건 및 우대사항 워드클라우드")
stop_words = ['가지', '회화', '학력', '경력', '심층', '학사이상', '익숙', '전반', '숙련', '실무']
visualize_wordcloud(data, font_path='C:/Windows/Fonts/malgun.ttf', stopwords=stop_words)