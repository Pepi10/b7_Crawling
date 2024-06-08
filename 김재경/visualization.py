import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

plt.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False
font_path = 'C:/Windows/Fonts/malgun.ttf'

def sales_distribution(data):
    """
    매출액 구간별 데이터 분포를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    """
    data2 = data.copy()
    data2['매출액'].fillna(0, inplace=True)


    categories = ['0-1억', '1-10억', '10-100억', '100-1000억', '1000억-1조', '1조-10조']

    money_len1 = len(data2[(data2['매출액'] >= 0) & (data2['매출액'] < 10000)])
    money_len2 = len(data2[(data2['매출액'] >= 10000) & (data2['매출액'] < 100000)])
    money_len3 = len(data2[(data2['매출액'] >= 100000) & (data2['매출액'] < 1000000)])
    money_len4 = len(data2[(data2['매출액'] >= 1000000) & (data2['매출액'] < 10000000)])
    money_len5 = len(data2[(data2['매출액'] >= 10000000) & (data2['매출액'] < 100000000)])
    money_len6 = len(data2[(data2['매출액'] >= 100000000) & (data2['매출액'] < 1000000000)])
    counts = [money_len1, money_len2, money_len3, money_len4, money_len5, money_len6]

    plt.figure(figsize=(10, 6)) 
    hist4 = plt.bar(categories, counts, color='blue', edgecolor='black', linewidth=1.2, alpha=0.7)  

    plt.xlabel('매출액 구간', fontsize=18, color='black')
    plt.ylabel('빈도', fontsize=18, color='black')
    plt.title('매출액 구간별 데이터 분포', fontsize=20, color='black', pad=20)
    plt.xticks(fontsize=20, color='black', rotation=45) 
    plt.yticks(fontsize=20, color='black')
    plt.grid(axis='y', linestyle='--') 
    plt.tight_layout()  
    plt.annotate('(단위: 개수)', xy=(0, 1), xytext=(-40, 15), xycoords='axes fraction', textcoords='offset points', ha='left', va='top', fontsize = 10)  # y축 단위 추가

    for p in hist4.patches:
        plt.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                 fontsize=12, color='black', ha='center', va='bottom')
    plt.show()

def establishment_year(data):
    """
    설립연도 데이터 분포를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    """

    plt.figure(figsize=(10, 6))
    hist = sns.histplot(data=data['설립연도'], bins=15, kde=True, color='darkgreen', edgecolor='black', linewidth=1.2, alpha=0.7) 
    plt.xlabel('설립연도', fontsize=18, color='black', labelpad=12)  
    plt.ylabel('빈도', fontsize=18, color='black', labelpad=12)  
    plt.title('설립연도 데이터 분포', fontsize=20, color='black', pad=20)
    plt.xticks(fontsize=20, color='black')
    plt.yticks(fontsize=20, color='black')  
    plt.tight_layout() 
    plt.grid(axis='y', linestyle='--')  
    plt.annotate('(단위: 년)', xy=(1, 0), xytext=(20, -35), xycoords='axes fraction', textcoords='offset points', ha='right', va='bottom', fontsize = 10)  
    plt.annotate('(단위: 개수)', xy=(0, 1), xytext=(-50, 25), xycoords='axes fraction', textcoords='offset points', ha='left', va='top', fontsize = 10) 

    for p in hist.patches:
        plt.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                 fontsize=12, color='black', ha='center', va='bottom')
    plt.show()

def position_years(data):
    """
    직급(연차)별 데이터 분포를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    """
 
    plt.figure(figsize=(10, 6)) 
    hist5 = sns.histplot(data=data['직급'], bins=10, kde=True, color='gold', edgecolor='black', linewidth=1.2, alpha=0.7)  # 히스토그램 스타일 설정
    plt.xlabel('직급(연차)', fontsize=18, color='black', labelpad=12) 
    plt.ylabel('빈도', fontsize=18, color='black', labelpad=12)  
    plt.title('직급(연차)별 데이터 분포', fontsize=20, color='black', pad=20)  
    plt.xticks(fontsize=20, color='black')
    plt.yticks(fontsize=20, color='black') 
    plt.tight_layout() 
    plt.grid(axis='y', linestyle='--') 
    plt.annotate('(단위: 년)', xy=(1, 0), xytext=(20, -35), xycoords='axes fraction', textcoords='offset points', ha='right', va='bottom', fontsize=10)  # x축 단위 추가
    plt.annotate('(단위: 개수)', xy=(0, 1), xytext=(-50, 25), xycoords='axes fraction', textcoords='offset points', ha='left', va='top', fontsize=10)  # y축 단위 추가

    for p in hist5.patches:
        plt.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                 fontsize=12, color='black', ha='center', va='bottom')

    plt.show()

def industry_distribution(data):
    """
    업종분류의 빈도를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    """
    company_counts = data['업종분류'].value_counts(sort=True)

    top_companies = company_counts.head(10)

    total_frequency = top_companies.sum()

    ratios = (top_companies / total_frequency) * 100

    plt.figure(figsize=(20, 12))
    bars = plt.barh(ratios.index[::-1], ratios.values[::-1], color='darkgreen', linewidth=0.1)  

    for i, bar in enumerate(bars):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{ratios[::-1][i]:.2f}%', va='center')  

    plt.title('상위 10개 업종분류의 비율', fontsize=40, color='black', pad=20)
    plt.xlabel('비율(%)', fontsize=20, color='black') 
    plt.ylabel('업종분류', fontsize=20, color='black') 
    plt.xticks(fontsize=20, color='black')
    plt.yticks(fontsize=20, color='black')
    plt.grid(axis='x', linestyle='--')
    plt.show()

def address(data):
    """
    주소 빈도수를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    """

    company_counts = data['주소'].value_counts(sort=True)

    top_companies = company_counts.head(10)

    total_frequency = top_companies.sum()

    ratios = (top_companies / total_frequency) * 100

    plt.figure(figsize=(20, 12))
    bars = plt.barh(ratios.index[::-1], ratios.values[::-1], color='blue', linewidth=0.1)  

    # 그래프 꾸미기
    for i, bar in enumerate(bars):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{ratios[::-1][i]:.2f}%', va='center')

    plt.title('상위 10개 업종분류의 비율', fontsize=40, color='black', pad=20)
    plt.xlabel('비율(%)', fontsize=20, color='black')  
    plt.ylabel('업종분류', fontsize=20, color='black') 
    plt.xticks(fontsize=20, color='black')
    plt.yticks(fontsize=20, color='black')
    plt.grid(axis='x', linestyle='--')
    plt.show()

def visualize_wordcloud(data, font_path, stopwords=None):
    """
    자격요건_키워드와 우대사항_키워드를 결합하여 워드클라우드를 시각화합니다.

    :param data: 시각화할 데이터 프레임
    :param font_path: 사용할 한글 폰트의 경로
    :param stopwords: 불용어 리스트
    """
    # 자격요건_키워드와 우대사항_키워드 컬럼을 합치기
    combined_keywords = data['자격요건_키워드'] + ' ' + data['우대사항_키워드']

    # 하나의 문자열로 합치기
    text = ' '.join(combined_keywords)

    # 워드클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path, stopwords=stopwords).generate(text)

    # 워드클라우드 그리기
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()