# 사용법 
# 크롬으로 쿠팡페이지 열기
# 크롬의 extenstion의 드래그프리 켜기(수동:단축키 alt+1)
# 가상 환경 설정 : conda activate py31012
# streamlit run cupang_r_maker_260322.py
import streamlit as st
from multiprocessing import freeze_support

from langchain_google_genai import ChatGoogleGenerativeAI #LLM Setting
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai

import time
import os
from dotenv import load_dotenv
import re

from langchain_ollama import ChatOllama
import ollama

def review_maker(prod,ex,selected_model,num=1000,comment=''):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 예제의 내용을 참고해서 만들고 또한 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 첫 문장은 전체 내용을 한 문장(20자 이내)으로 요약해서 출력합니다.  
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 3학년,초등학생 5학년)을 키우는 40대 중반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        5) example을 참고해서 리뷰를 작성합니다.
        6) comment가 있는 경우 이 내용은 반드시 포함해서 작성합니다.
        
        [example]
        example 1) {ex0}
        example 2) {ex1}
        example 3) {ex2}
        example 4) {ex3}
        example 5) {ex4}
        
        [comment]
        {comment}
        """
        
        ) 
        | ChatGoogleGenerativeAI(model=selected_model, temperature = 0.1) 
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke(
        {"product": prod, "ex0": ex[0], "ex1": ex[1], "ex2": ex[2], "ex3": ex[3], "ex4": ex[4], "num": num, "comment": comment})
    st.write(resonse)

def review_maker_new(prod,ex,selected_model,num=1500,comment=''):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 예제의 내용을 참고해서 만들고 또한 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 첫 문장은 전체 내용을 한 문장(20자 이내)으로 요약해서 출력합니다.  
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 3학년,초등학생 5학년)을 키우는 40대 중반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        5) example을 참고해서 리뷰를 작성합니다.
        6) comment가 있는 경우 이 내용은 반드시 포함해서 작성합니다.
        7) 물품을 무료로 제공받아 작성하는 쿠팡 체험단의 글이니 구매나 가격의 이야기는 제외합니다.
        
        [example]
        example 1) {ex0}
        example 2) {ex1}
        example 3) {ex2}
        example 4) {ex3}
        example 5) {ex4}

        [comment]
        {comment}
        """
        ) 
        | ChatGoogleGenerativeAI(model=selected_model, temperature = 0.1) 
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke(
        {"product": prod, "ex0": ex[0], "ex1": ex[1], "ex2": ex[2], "ex3": ex[3], "ex4": ex[4], "num": num, "comment": comment})
    st.write(resonse)

def review_maker_ollama(prod,ex,selected_model,num=1000,comment=''):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 예제의 내용을 참고해서 만들고 또한 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 첫 문장은 전체 내용을 한 문장(20자 이내)으로 요약해서 출력합니다.  
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 3학년,초등학생 5학년)을 키우는 40대 중반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        5) example을 참고해서 리뷰를 작성합니다.
        6) comment가 있는 경우 이 내용은 반드시 포함해서 작성합니다.
                
        [example]
        example 1) {ex0}
        example 2) {ex1}
        example 3) {ex2}
        example 4) {ex3}
        example 5) {ex4}
        [comment]
        {comment}
        """
        ) 
        | ChatOllama(model=selected_model,temperature = 0.1)
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke(
        {"product": prod, "ex0": ex[0], "ex1": ex[1], "ex2": ex[2], "ex3": ex[3], "ex4": ex[4], "num": num})
    st.write(resonse)

def review_maker_ollama_new(prod,ex,selected_model,num=1500,comment=''):

    # LCEL chaining
    chain = (
        ChatPromptTemplate.from_template(
        """
        당신은 쿠팡에서 {product}을 구매한 후에 {product}을 사용해 보고 {product}의 리뷰를 작성하는 인공지능 챗봇입니다.
        리뷰는 예제의 내용을 참고해서 만들고 또한 규칙을 지켜서 작성해야 합니다.

        [규칙]
        1) 첫 문장은 전체 내용을 한 문장(20자 이내)으로 요약해서 출력합니다.  
        2) 전체 글자수는 {num}자 이하로 작성해야 합니다.
        3) 남자 아이 두명(중학교 3학년,초등학생 5학년)을 키우는 40대 중반의 주부라고 생각하고 작성해야 합니다.
        4) 장점과 단점을 구분해서 작성해야 합니다.
        5) example을 참고해서 리뷰를 작성합니다.
        6) comment가 있는 경우 이 내용은 반드시 포함해서 작성합니다.
        7) 물품을 무료로 제공받아 작성하는 쿠팡 체험단의 글이니 구매나 가격의 이야기는 제외합니다.
                
        [example]
        example 1) {ex0}
        example 2) {ex1}
        example 3) {ex2}
        example 4) {ex3}
        example 5) {ex4}
        [comment]
        {comment}
        """
        ) 
        | ChatOllama(model=selected_model,temperature = 0.1)
        | StrOutputParser()
    )
    # chain 호출
    resonse = chain.invoke(
        {"product": prod, "ex0": ex[0], "ex1": ex[1], "ex2": ex[2], "ex3": ex[3], "ex4": ex[4], "num": num})
    st.write(resonse)


if __name__ == "__main__":

    # GOOGLE_API_KEY 환경 변수 값 가져오기
    google_api_key = os.getenv('GOOGLE_API_KEY')

    # genai.configure로 GOOGLE API KEY Setting하기기
    genai.configure(api_key=google_api_key)

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

    if "reviews0" not in st.session_state:
        st.session_state.reviews0 = ''
    
    if "reviews1" not in st.session_state:
        st.session_state.reviews0 = ''

    if "reviews2" not in st.session_state:
        st.session_state.reviews0 = ''
    
    if "reviews3" not in st.session_state:
        st.session_state.reviews0 = ''

    if "reviews4" not in st.session_state:
        st.session_state.reviews0 = ''

    if "llm_model_option" not in st.session_state:
        st.session_state.llm_model_option = ''
    
    if "max_text_length" not in st.session_state:
        st.session_state.max_text_length = 0

    if "comment" not in st.session_state:
        st.session_state.comment = ''

    if "option" not in st.session_state:
        st.session_state.option = ''

    if "bf_time" not in st.session_state:
        st.session_state.bf_time = 0

    if "total_time" not in st.session_state:
        st.session_state.total_time = 0


    with st.sidebar:

        st.subheader('LLM Model을 선택하기')

        st.session_state.llm_model_option = st.radio(
            'LLM 종류를 선택하세요.:',('Ollama', 'Gemini',))

        if st.session_state.llm_model_option == 'Ollama':

            model_name = []

            models = ollama.list()

            # 모델 목록 출력하기
            for model in models['models']:
                model_name.append(model['model'])

            selected_model = st.sidebar.selectbox('Choose Ollama Model', 
                                                  model_name,key='selected_model')
            
            st.info(f'{selected_model}을 선택하셨습니다.')

        elif st.session_state.llm_model_option == 'Gemini':

            model_name = []

            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    model_name.append(re.sub(r'models/','',model.name))

            st.subheader('Gemini Model을 선택하세요.')
            #selected_model = st.sidebar.selectbox('Choose Gemini Model', ['gemini-1.5-flash',  'gemini-1.        5-flash-latest','gemini-1.5-pro', 'gemini-1.5-pro-latest'], key='selected_model')
            selected_model = st.sidebar.selectbox('Choose Gemini Model', model_name
                                                      , key='selected_model')
        
            st.info(f'{selected_model}을 선택하셨습니다.')

        "[참고 자료 1](https://blog.naver.com/PostView.naver?blogId=itandtech&logNo=223624403146)"
        "[참고 자료 2](https://ai.google.dev/gemini-api/docs/models/gemini?hl=ko)"
    

    st.header("**:blue[_쿠팡_] :red[_Reviews_] Maker** :sunglasses:")
    st.subheader(f"쿠팡 리뷰를 검색하고 AI로 리뷰를 작성합니다.")

    load_dotenv()

    st.session_state.reviews0 = st.text_input("첫번째 Review를 작성해주세요.")

    if not st.session_state.reviews0:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()

    st.session_state.reviews1 = st.text_input("2번째 Review를 작성해주세요.")

    if not st.session_state.reviews1:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()

    st.session_state.reviews2 = st.text_input("3번째 Review를 작성해주세요.")

    if not st.session_state.reviews2:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()

    st.session_state.reviews3 = st.text_input("4번째 Review를 작성해주세요.")

    if not st.session_state.reviews3:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()

    st.session_state.reviews4 = st.text_input("5번째 Review를 작성해주세요.")

    if not st.session_state.reviews4:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()

    st.session_state.comment = st.text_input("꼭 넣어야할 커멘트가 있다면 입력해 주세요.")

    st.session_state.reviews = [st.session_state.reviews0, st.session_state.reviews1, st.session_state.reviews2, st.session_state.reviews3, st.session_state.reviews4]

    if len(st.session_state.reviews) < 5:
        st.warning("리뷰를 입력해 주세요.")
        st.stop()
     
    st.session_state.option = st.radio('리뷰 종류를 선택하세요.:',('일반', '체험단',))

    st.session_state.max_text_length = st.radio('글자수를 선택하세요.:',(1000, 1500,))

    st.info('참고 review')
    st.write(st.session_state.reviews[0])

    if prod := st.text_input('제품명을 입력하세요. 일반단어로 표현해 주세요 ex) 샘표간장(x), 간장(o) >>>   '):
        
        st.info(f'{st.session_state.option}을 선택하셨고 {st.session_state.max_text_length}자의 리뷰를 생성합니다.')

        st.session_state.bf_time = time.time()

        st.subheader("기존 Review를 참고하여 작성한 리뷰입니다.")
        if st.session_state.llm_model_option == 'Gemini':
            if st.session_state.option == '일반':
                review_maker(prod,st.session_state.reviews,selected_model,
                             st.session_state.max_text_length,st.session_state.comment)
            else:
                review_maker_new(prod,st.session_state.reviews,selected_model,
                                 st.session_state.max_text_length,st.session_state.comment)

        elif st.session_state.llm_model_option == 'Ollama':
            if st.session_state.option == '일반':
                review_maker_ollama(prod,st.session_state.reviews,selected_model,
                                    st.session_state.max_text_length,st.session_state.comment)
            else:
                review_maker_ollama_new(prod,st.session_state.reviews,selected_model,
                                 st.session_state.max_text_length,st.session_state.comment)

        st.session_state.total_time = time.time() - st.session_state.bf_time
        st.info("리뷰 생성이 완료 됐습니다.")
        st.success(f"Total {st.session_state.total_time}초 소요 되었습니다.", icon="✅")