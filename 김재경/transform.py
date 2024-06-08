import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import (LatentDirichletAllocation, 
                                   TruncatedSVD)
from konlpy.tag import Okt

def convert_experience(exp_str):
    """
    경력 전처리 함수
    신입 = 0
    범위 = avg 
    """
    numbers = re.findall(r'\d+', exp_str)
    if len(numbers) == 2:
        average_exp = (int(numbers[0]) + int(numbers[1])) / 2
        return int(average_exp)
    elif len(numbers) == 1:
        return int(numbers[0])
    else:
        return 0

def run_preprocess_career(df):
    processed_career = []
    for career in df.직급:
        processed_career.append(convert_experience(career))
    df.직급 = processed_career

def preprocess_address(df):
    address_list = []
    for address in df.주소:
        if '경기' in address and '경기도' not in address:
            address = re.sub('경기', '경기도', address)
        elif '서울' in address and '서울특별시' not in address and '서울시' not in address:
            address = re.sub('서울', '서울특별시', address)
        elif '서울시' in address and '서울특별시' not in address:
            address = re.sub('서울시', '서울특별시', address)     
        elif '강남구' in address and '서울특별시' not in address and '서울' not in address:
            address = re.sub('강남구', '서울특별시 강남구', address)
        elif '서초구' in address and '서울특별시' not in address and '서울' not in address:
            address = re.sub('서초구', '서울특별시 서초구', address)
        elif '중구' in address and '서울특별시' not in address and '서울' not in address:
            address = re.sub('중구', '서울특별시 중구', address)
        elif '용산구' in address and '서울특별시' not in address and '서울' not in address:
            address = re.sub('용산구', '서울특별시 용산구', address)
        elif '마포구' in address and '서울특별시' not in address and '서울' not in address:
            address = re.sub('마포구', '서울특별시 마포구', address)
        elif '성남시' in address and '경기도' not in address:
            address = re.sub('성남시', '경기도 성남시', address)
        # 수정된 부분: 위의 조건들에 해당하지 않는 경우에도 그대로 유지합니다.
        
        # 수정된 부분: 주소를 address_list에 추가합니다.
        address_list.append(address)

    add_list = []
    for address in address_list:
        # 수정된 부분: 주소가 처리되지 않은 경우 None을 추가합니다.
        if address:
            # 수정된 부분: 주소에서 시, 구, 도만 추출하여 리스트에 추가합니다.
            add_list.append(' '.join(re.findall(r'\b(\w+[천구시도])\b', address)))
        else:
            add_list.append(None)

    df.주소 = add_list
    empty_address_indices = df[df['주소'] == ''].index
    df.drop(empty_address_indices, inplace=True)


class TextProcessor_1:
    def __init__(self):
        pass
    
    def preprocess_text(self, text):
        """
        텍스트 전처리 함수
        """
        text = text.replace('•', ' ')
        return text

    def vectorize_text(self, text_data, max_features=20):
        """
        TF-IDF 벡터화 함수
        """
        vectorizer = TfidfVectorizer(max_features=max_features)
        X = vectorizer.fit_transform(text_data)
        return X, vectorizer
    
    def reduce_dimensions(self, X, n_components=10, random_state=77):
        """
        차원 축소 함수
        """
        svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        X_reduced = svd.fit_transform(X)
        return X_reduced, svd
    
    def get_top_keywords(self, model, feature_names, n_top_words):
        """
        주요 키워드 추출 함수
        """
        top_keywords = []
        for topic_idx, topic in enumerate(model.components_):
            top_keywords.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        return top_keywords

    def process_text_data(self, text_data, max_features=20, n_components=10, n_top_words=6):
        """
        텍스트 데이터 처리 함수
        """
        preprocessed_text = text_data.apply(self.preprocess_text)
        X, vectorizer = self.vectorize_text(preprocessed_text, max_features)
        X_reduced, svd = self.reduce_dimensions(X, n_components)
        feature_names = vectorizer.get_feature_names_out()
        top_keywords = self.get_top_keywords(svd, feature_names, n_top_words)
        return X_reduced, top_keywords
    
class TextProcessor_2:
    def __init__(self):
        self.korean_stop_words = ['조직', '개인', '장소', '통합', '과제', '실력', '전체', '보이시', '근거', '중심', '후보자', '초기', '부담', '흥미', '기반시설', '태도', '기본', '희망', '국한', '회로', '처음', '방안', '통한', '위해', '자기', '노력', '사용자', '대해', '목표', '스스로', '성향', '지향', '참여', '테스트', '역량', '전형', '중요성', '작성', '적용', '습득', '고객', '용량', '방식', '신분', '관리', '적극', '서비스', '업무', '가능', '기반', '이용', '진행', '포함', '기술', '처리', '활용', '재현', '졸업', '이해도', '사용', '코드', '관심', '근무', '이해', '운영', '이상', '경력', '관련', '및', '있는', '또는', '등', '대한', '및', '관련', '개발', '경험', '분', '분야', '관련', '보유', '우대', '환경', '전공', '우대']
        self.english_stop_words = 'english'
        self.word_mapping = {
            '티스': '쿠버네티스',
            '쿠버': '쿠버네티스',
            '러닝': '딥러닝',
            '머신': '머신러닝',
            '보수': '유지보수',
            '분산': '분산처리'
        }
    
    def preprocess_text(self, text):
        okt = Okt()
        tokens = okt.nouns(text)  # 명사 추출
        return ' '.join(tokens)

    def apply_word_mapping(self, keywords):
        mapped_keywords = [self.word_mapping.get(word, word) for word in keywords]
        return list(set(mapped_keywords)) 

    def process_data(self, data):
        processed_data = data.apply(lambda x: self.preprocess_text(x['이용하는기술스택/우대사항']), axis=1)
        stop_words = self.korean_stop_words + list(TfidfVectorizer(stop_words=self.english_stop_words).get_stop_words())
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_matrix = vectorizer.fit_transform(processed_data)
        lda = LatentDirichletAllocation(n_components=len(data), random_state=777)
        lda.fit(tfidf_matrix)
        
        def get_top_keywords(model, feature_names, n_top_words):
            keywords = []
            for topic_idx, topic in enumerate(model.components_):
                top_keywords = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
                keywords.append(top_keywords)
            return keywords
        
        feature_names = vectorizer.get_feature_names_out()
        top_keywords = get_top_keywords(lda, feature_names, 5)
        
        data['우대사항_키워드'] = None
        for idx, keywords in enumerate(top_keywords):
            mapped_keywords = self.apply_word_mapping(keywords)
            data.at[idx, '우대사항_키워드'] = ', '.join(mapped_keywords)
        
        return data