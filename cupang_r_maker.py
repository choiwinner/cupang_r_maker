# streamlit run cupang_r_maker.py
import streamlit as st
#multiprocess error
from multiprocessing import freeze_support

from langchain_google_genai import ChatGoogleGenerativeAI #LLM Setting
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 

import time
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options



import google.generativeai as genai

def review_maker(prod,ex,selected_model,num=500):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 예제의 내용을 참고해서 만들고 또한 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 리뷰는 반드시 아래 문장으로 시작해야 합니다.
        - 이번에 구매하게 된 {product}에 대한 사용기에 대해 말씀드릴께요.
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 2학년,초등학생 4학년)을 키우는 40대 초반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        5) example을 참고해서 리뷰를 작성합니다.
        
        [example]
        example 1) {ex0}
        example 2) {ex1}
        example 3) {ex2}
        example 4) {ex3}
        example 5) {ex4}
        """
        ) 
        | ChatGoogleGenerativeAI(model=selected_model, temperature = 0.1) 
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke(
        {"product": prod, "ex0": ex[0], "ex1": ex[1], "ex2": ex[2], "ex3": ex[3], "ex4": ex[4], "num": num})
    st.write(resonse)

def review_maker2(prod,selected_model,num=500):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 리뷰는 반드시 아래 문장으로 시작해야 합니다.
        - 이번에 구매하게 된 {product}에 대한 사용기에 대해 말씀드릴께요.
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 2학년,초등학생 4학년)을 키우는 40대 초반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        
        """
        ) 
        | ChatGoogleGenerativeAI(model=selected_model, temperature = 0.1) 
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke({"product": prod, "num": num})
    st.write(resonse)
    

@st.cache_data()
def hold(hold_v):
    if(hold_v == 'OK'):
        st.write('사용자님 환영합니다.')
    else:
        st.error("잘못된 입력입니다. 다시 입력해 주세요.")
        st.stop()

@st.cache_data()
def cupang_crwal(URL):

    # 크롬 드라이버 경로 설정
    options = Options() 
    #options = webdriver.ChromeOptions()

    options.add_argument('--headless=new')           #Streamlit Cloud에서 Selenium WebDriver 에러를 해결
    options.add_argument('--disable-gpu')            #Streamlit Cloud에서 Selenium WebDriver 에러를 해결
    options.add_argument('--no-sandbox')             #Streamlit Cloud에서 Selenium WebDriver 에러를 해결   
    options.add_argument('--disable-dev-shm-usage')  #Streamlit Cloud에서 Selenium WebDriver 에러를 해결

    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,   like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 쿠팡 상품 페이지 열기
    driver.get(URL)

    # 페이지 로딩 대기(5초)
    time.sleep(5) 
    
    # bs4로 리뷰 찾기
    html = driver.page_source
    soup = bs(html, 'html.parser')
    result = soup.select('div.sdp-review__article__list__review__content')

    count = len(result) #review 개수 확인

    if count >=5:
        st.info(f'{count}의 Review가 성공적으로 검색되었습니다.')

    else:
        st.error(f"{count}개 Review가 검색되어 소스코드 수정 필요합니다.(5개 미만만)")
        st.stop()

    reviews = []

    for i in range(count):
        reviews.append(result[i].getText().strip())
    
    return reviews
    
if __name__ == "__main__":

    freeze_support() # for multiprocessing other process on windows

    # 페이지 기본 설정
    st.set_page_config(
        page_title="🔎쿠팡 리뷰 Maker",
        layout="wide",
        initial_sidebar_state="expanded")

    if "reviews" not in st.session_state:
        st.session_state.reviews = []
    if "url" not in st.session_state:
        st.session_state.url = None
    
    if "gemini" not in st.session_state:
        st.session_state.gemini_api_key = None
    
    #hold_v = 'No'

    with st.sidebar:
        st.session_state.gemini_api_key = st.text_input('Gemini_API_KEY를 입력하세요.', key="langchain_search_api_gemini", type="password")
        "[Get an Gemini API key](https://ai.google.dev/)"
        "[How to get Gemini API Key](https://luvris2.tistory.com/880)"

        if (st.session_state.gemini_api_key[0:2] != 'AI') or (len(st.session_state.gemini_api_key) != 39):
            st.warning('잘못된 key 입력', icon='⚠️')
        else:
            st.success('정상 key 입력', icon='👉')

        if process :=st.button("Process"):
            if (st.session_state.gemini_api_key[0:2] != 'AI') or (len(st.session_state.gemini_api_key) != 39):
                st.error("잘못된 key 입력입니다. 다시 입력해 주세요.")
                st.stop()

        #random_val = int(st.text_input('문제를 선택하시오 0~10번 선택'))
#
        #if random_val==0:
        #    namex = st.text_input('24년 9월 기준 김여사가 다니는 직장은? 9글자 ㅇㅇㅇㅇㅇㅇㅇ병원')
        #    if process :=st.button("Process"):
        #        if (namex != '세종충남대학교병원'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
        #    
        #if random_val==1:
        #    namex = st.text_input('24년 9월 기준 김여사가 가장 좋아하는 배우는? 3글자 김ㅇㅇ')
        #    if process :=st.button("Process"):
        #        if (namex != '김혜윤'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==2:
        #    namex = st.text_input('24년 9월 기준 김여사가 다니는 교회는? 6글자 ㅇㅇㅇㅇ교회')
        #    if process :=st.button("Process"):
        #        if (namex != '세종한빛교회'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==3:
        #    namex = st.text_input('24년 9월 기준 김여사의 사는 동이름은? 3글자 ㅇㅇ동')
        #    if process :=st.button("Process"):
        #        if (namex != '나성동'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==4:
        #    namex = st.text_input('24년 봄 김여사가 여행한 나라는? 2글자 ㅇㅇ')
        #    if process :=st.button("Process"):
        #        if (namex != '대만'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
        #    
        #if random_val==5:
        #    namex = st.text_input('김여사의 생년월일은? 숫자 8개만 입력 19ㅇㅇㅇㅇㅇㅇ')
        #    if process :=st.button("Process"):
        #        if (namex != '19810609'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==6:
        #    namex = st.text_input('24년 9월 기준 김여사가 가장 좋아하는 드라마는? 6글자 ㅇㅇㅇㅇㅇㅇ')
        #    if process :=st.button("Process"):
        #        if (namex != '선재업고튀어'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==7:
        #    namex = st.text_input('24년 9월 기준 김여사의 직업은? 7글자 ㅇㅇㅇㅇ연구원')
        #    if process :=st.button("Process"):
        #        if (namex != '임상배아연구원'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==8:
        #    namex = st.text_input('김여사가 고등학교 시절 좋아했던 가수는? 3글자 ㅇㅇㅇ')
        #    if process :=st.button("Process"):
        #        if (namex != '김종서'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'            
#
        #if random_val==9:
        #    namex = st.text_input('김여사가 목장모임을 하는 장소는? 5글자 ㅇㅇㅇ센터')
        #    if process :=st.button("Process"):
        #        if (namex != '놀뛰날센터'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'
#
        #if random_val==10:
        #    namex = st.text_input('김여사의 고등학교 시절 최고의 발명품은? 4글자 ㅇㅇ집게')
        #    if process :=st.button("Process"):
        #        if (namex != '꼼꼼집게'):
        #            st.error("잘못된 사용자입니다. 다시 입력해 주세요.")
        #            hold_v = 'NO'
        #            st.stop()
        #        else:
        #            hold_v = 'OK'

    st.header("**:blue[_쿠팡_] :red[_Revies_] Maker** :sunglasses:")
    st.subheader(f"쿠팡 리뷰를 검색하고 AI로 리뷰를 작성합니다.")

    #0. gemini api key Setting
    if not st.session_state.gemini_api_key:
        st.warning("Gemini API Key를 입력해 주세요.")
        st.stop()

    #0. gemini api key Setting
    os.environ["GOOGLE_API_KEY"] = st.session_state.gemini_api_key

    #if namex:
    #    hold_v = 'OK'

    #st.write(hold_v)

    #hold(hold_v)

    st.session_state.url = st.text_input('원하시는 상품의 URL 주소를 입력해주세요\n\nEx)\nhttps://www.coupang.com/vp/products/7335597976?itemId=18741704367&vendorItemId=85873964906&q=%ED%9E%98%EB%82%B4%EB%B0%94+%EC%B4%88%EC%BD%94+%EC%8A%A4%EB%8B%88%EC%BB%A4%EC%A6%88&itemsCount=36&searchId=0c5c84d537bc41d1885266961d853179&rank=2&isAddedCart=:')

    #st.session_state.url = 'https://www.coupang.com/vp/products/7040671922'

    if not st.session_state.url:
        st.warning("url을 입력해 주세요.")
        st.stop()

    st.session_state.reviews = cupang_crwal(st.session_state.url)

    selected_model = st.radio('Choose Gemini Model', ['gemini-1.5-flash', 'gemini-1.5-flash-latest','gemini-1.5-pro', 'gemini-1.5-pro-latest','gemini-2.0-flash-exp'], key='selected_model')

    st.info(f'{selected_model}을 선택하셨습니다.')
    
    selected_option = st.radio(
        '리뷰 종류를 선택하세요.:',('일반', '체험단',))

    if selected_option == '일반':
        num = 1000
    elif selected_option == '체험단':
        num = 1500

    st.info('참고 review')
    st.write(st.session_state.reviews[0])
    #st.write(st.session_state.reviews[1])
    #st.write(st.session_state.reviews[2])

    if prod := st.text_input('제품명을 입력하세요. 일반단어로 표현해 주세요 ex) 샘표간장(x), 간장(o) >>>   '):

        
        st.info(f'{selected_option}을 선택하셔서 {num}자의 리뷰를 생성합니다.')

        st.subheader("기존 Review를 참고하여 작성한 리뷰입니다.")
        review_maker(prod,st.session_state.reviews,selected_model,num)
        #st.subheader("기존 Review를 참고하지 않고 작성한 리뷰입니다.")
        #review_maker2(prod,selected_model,num) 
        st.info("리뷰 생성이 완료 됐습니다.")