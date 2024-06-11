# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 17:52:28 2024

@author: lcsdc
"""

import streamlit as st
import pandas as pd
from PIL import Image

def run_home(total_df):
    img = Image.open('pic1.png')
    img2 = Image.open('pic2.png')
    st.markdown("# 데이터 소개 \n")
    st.markdown("1. 본 프로젝트에 사용된 데이터는 서울시 생필품 농수축산물 정보를 제공합니다. \n"
                "2. 서울시 물가모니터가 주1회 자치구별 전통시장에 나가 농수축산물 16개 품목을 조사하고 그 가격을 공개하는 정보입니다. \n "
                "3. 위 데이터는 40000개 사용되었습니다.")
    st.image(img)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## 출력값 \n")
    st.image(img2)
    st.markdown("<hr>", unsafe_allow_html=True)


    nm = st.sidebar.selectbox("자치구", total_df['M_GU_NAME'].unique())
    
    month_dic = {'1월': 1, '2월': 2, '3월': 3, '4월': 4, '5월': 5, '6월': 6,
                 '7월': 7, '8월': 8, '9월': 9, '10월': 10, '11월': 11, '12월': 12}

    selected_month = st.sidebar.selectbox("확인하고 싶은 월을 선택하시오.", list(month_dic.keys()))

    # P_DATE 열을 datetime으로 변환
    total_df['P_DATE'] = pd.to_datetime(total_df['P_DATE'], format='%Y-%m-%d')


    # 선택한 자치구, 연도, 월로 데이터 필터링
    filtered_df = total_df[(total_df['M_GU_NAME'] == nm) & 
                           (total_df['P_DATE'].dt.month == month_dic[selected_month])]

    # 선택한 자치구, 연도, 월에 대한 정보 표시
    st.subheader(f'{nm} 2024년 {selected_month} 데이터 확인하기')
    st.write(filtered_df)


