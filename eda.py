
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from viz import showViz
from statistic import showStat
from statistic2 import showStat2

def home() :
    st.markdown("### 1. Visualization \n"
                "##### 자치구의 품목별 월별 평균 가격 추이 선그래프 \n"
                "- option: 자치구 선택, 품목 이름 선택  \n"
                "**1. 일반 사용자가 가격 변동을 쉽게 이해할 수 있도록 시각화**  \n"
                "**2. 월별 시장 트렌드 파악 가능**  \n")
    st.markdown("### 2. Statistics \n"
                "##### 품목별로 자치구 간 물가 영향력을 파악할 수 있는 상관계수를 확인 \n"
                "- option: 첫 번째 자치구 선택, 두 번째 자치구 선택, 품목 이름 선택 \n "
                "- 두 자치구가 동일하다면 메세지 출력  \n"
                "**1. 서로 다른 지역 간의 물가 동향을 비교, 물가 변동이 더 민감한지, 더 안정적인지 등을 확인**  \n"
                "**2. 지역 경제의 특성 이해, 유사 혹은 대조적 소비 패턴, 시장 조건을 가지고 있을 수 있음을 시사**  \n"
                "**3. 한 자치구에서의 물가 변동이 다른 자치구에도 영향을 미칠 수 있음을 의미**  \n")
    st.markdown("### 3. Statistics2 \n"
                "##### 자치구별로 품목 간 물가 영향력을 파악할 수 있는 상관계수를 확인 \n"
                "- option: 첫 번째 품목 선택, 두 번째 품목 선택, 해당 자치구 선택 \n "
                "- 두 품목 동일하다면 메세지 출력  \n"
                "**1. 소비자들의 소비 트렌드와 선호도 파악, 두 제품 간의 상호 대체성이 높거나 낮을 수 있음을 시사**  \n"
                "**2. 경제적 영향을 파악, 특정 품목의 물가 상승이 다른 품목의 물가에 어떤 영향을 미치는지를 이해**  \n"
                "**3. 두 제품 간의 관련성을 이해 구매 결정 가능, 비슷한 기능을 제공하는 두 제품 중 소비자들은 더 저렴한 제품 선택**  \n")


def run_eda(total_df):
    st.markdown('# 상관관계 분석 \n')
    
    selected = option_menu(None, ['Home', 'Visualization', 'Statistics', 'Statistics2'],
                           icons=['house', 'bar-chart', 'file-spreadsheet', 'file-spreadsheet'],
                           menu_icon='cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                   'padding' : '0!important',
                                   'background-color' : '#e0e1dd'},
                               'icon' : {
                                   'color' : '#ffffff',
                                   'font-size' : '25px'},
                               'nav-link' : {
                                   'font-size' : '15px',
                                   'text-align' : 'left',
                                   'margin' : '0px',
                                   '--hover-color' : '#eee'},
                               'nav-link-selected' : {
                                   'background-color' : '#778da9'}
                               })
    
                           
    if selected == 'Home':
        home()
    elif selected == 'Visualization':
        showViz(total_df)
    elif selected == 'Statistics':
        showStat(total_df)
    elif selected == 'Statistics2':
        showStat2(total_df)
    else:
        st.warning('Wrong')