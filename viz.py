# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 17:52:28 2024

@author: lcsdc
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def priceTrend(total_df, nm, a_name):
    st.markdown(f'### {nm}의 {a_name} 월별 평균 가격 추이 \n')
    
    # 선택한 자치구와 품목으로 데이터 필터링
    filtered_df = total_df[(total_df['M_GU_NAME'] == nm) & (total_df['A_NAME'] == a_name)]
    
    # 월별 평균 가격 계산
    filtered_df['P_DATE'] = pd.to_datetime(filtered_df['P_DATE'])
    filtered_df['YearMonth'] = filtered_df['P_DATE'].dt.to_period('M').astype(str)  # Period를 문자열로 변환
    result = filtered_df.groupby('YearMonth')['A_PRICE'].mean().reset_index()
    
    # 그래프 생성
    fig = px.line(result, x='YearMonth', y='A_PRICE')
    fig.update_yaxes(title_text='가격(원)')
    fig.update_xaxes(title_text='월')
    fig.update_layout(width=800, height=600, template='plotly_white')
    
    st.plotly_chart(fig)

def showViz(total_df):
    total_df['P_DATE'] = pd.to_datetime(total_df['P_DATE'], format='%Y-%m-%d')
    
    # 자치구와 품목 선택
    nm = st.sidebar.selectbox("자치구", total_df['M_GU_NAME'].unique())
    a_name = st.sidebar.selectbox("품목 이름", total_df['A_NAME'].unique())
    
    # 선택한 자치구와 품목에 대한 월별 평균 가격 추이 그래프 표시
    priceTrend(total_df, nm, a_name)

