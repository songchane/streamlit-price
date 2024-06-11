# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 16:26:44 2024

@author: lcsdc
"""

import streamlit as st
from streamlit_option_menu import option_menu
from utils import load_data


from home import run_home
from eda import run_eda
from ml import run_ml
from donut import run_donut


def main():
    total_df = load_data()    
    
    with st.sidebar:
        selected = option_menu('물가 데이터', ['홈', '상관관계 분석', '물가 예측', '요소 분석'],
                               icons=['house', 'file-bar-graph', 'graph-up-arrow'], menu_icon='cast', default_index=0,
                               styles={
                                   'nav-link-selected' : {
                                   'background-color' : '#778da9'}                                   
                               })
        
            


        
    if selected == '홈':
        run_home(total_df)
    elif selected == '상관관계 분석' :
        run_eda(total_df)
    elif selected == '물가 예측':
        run_ml(total_df)
    elif selected == '요소 분석':
        run_donut(total_df)
    else:
        print('error')
            
if __name__ == "__main__":
    main()