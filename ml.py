import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import datetime

import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.font_manager as fm

# 한글 폰트 설정 (필요한 경우)
def set_font():
    path = 'NanumGothic-Bold.ttf'
    fontprop = fm.FontProperties(fname=path, size=12)
    plt.rcParams['font.family'] = fontprop.get_name()
    
def home():
    st.markdown("### 1. 품목별 \n"
                "##### 품목별 평균가를 분석하여 품목의 물가를 예측 \n"
                "- option: 예측할 품목 선택, 예측 기간 선택  \n"
                "**1. 소비자 및 생산자의 관심을 끌고, 시장 동향을 예측하는 역할**  \n"
                "**2. 소비자는 소비 패턴을 조정하고 기업은 생산 및 가격 전략을 재조정**  \n")
    st.markdown("### 2. 자치구별 \n"
                "##### 자치구별 품목 평균가를 분석하여 자치구의 물가를 예측 \n"
                "- option: 예측할 자치구 선택, 예측 기간 선택  \n"
                "**1. 특정 지역의 소비 트렌드 및 경제적 상황을 이해하는 데 도움**  \n"
                "**2. 지역 기업 및 정부에게 지역 경제를 적극적으로 관리하고 지역 발전을 촉진하는 데 도움**  \n")
    st.markdown("### 3. 보고서 \n"
                "##### 자치구와 품목을 선택하여 해당하는 옵션의 물가를 선택적으로 예측 \n"
                "- option: 자치구 선택, 품목 선택, 예측 기간 선택  \n"
                "**1. 예측 결과를 종합적으로 정리하여 사용자에게 제공**  \n"
                "**2. 좀 더 세부적이고 선택적으로 물가 예측 결과를 확인 및 저장**  \n")
    
def predict_by_item(df):
    set_font()
    
    df['P_DATE'] = pd.to_datetime(df['P_DATE'], format='%Y-%m-%d')
    items = df['A_NAME'].unique()
    
    selected_item = st.sidebar.selectbox('예측할 품목을 선택하세요', items)
    periods = st.sidebar.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)', min_value=1, max_value=30, step=1)
    
    df_item = df[df['A_NAME'] == selected_item]
    summary_df = df_item.groupby('P_DATE')['A_PRICE'].mean().reset_index()
    summary_df = summary_df.rename(columns={'P_DATE': 'ds', 'A_PRICE': 'y'})
    
    model = Prophet()
    model.fit(summary_df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    fig = model.plot(forecast)
    plt.title(f'{selected_item} 가격 예측 {periods}일간', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    plt.xlabel('날짜', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    plt.ylabel('가격(원)', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    st.pyplot(fig)
    
def predict_by_district(df):
    set_font()
    
    df['P_DATE'] = pd.to_datetime(df['P_DATE'], format='%Y-%m-%d')
    districts = df['M_GU_NAME'].unique()
    
    selected_district = st.sidebar.selectbox('예측할 자치구를 선택하세요', districts)
    periods = st.sidebar.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)', min_value=1, max_value=30, step=1)
    
    df_district = df[df['M_GU_NAME'] == selected_district]
    summary_df = df_district.groupby('P_DATE')['A_PRICE'].mean().reset_index()
    summary_df = summary_df.rename(columns={'P_DATE': 'ds', 'A_PRICE': 'y'})
    
    model = Prophet()
    model.fit(summary_df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    fig = model.plot(forecast)
    plt.title(f'{selected_district} 평균 물가 예측 {periods}일간', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    plt.xlabel('날짜', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    plt.ylabel('평균 물가(원)', fontproperties=fm.FontProperties(fname='NanumGothic-Bold.ttf'))
    st.pyplot(fig)

def report_main(df):
    set_font()
    
    df['P_DATE'] = pd.to_datetime(df['P_DATE'], format='%Y-%m-%d')
    districts = df['M_GU_NAME'].unique()
    items = df['A_NAME'].unique()
    
    selected_district = st.sidebar.selectbox('자치구', districts)
    selected_item = st.sidebar.selectbox('품목', items)
    periods = st.sidebar.number_input('향후 예측 기간을 지정하세요(1일 ~ 30일)', min_value=1, max_value=30, step=1)

    df_filtered = df[(df['M_GU_NAME'] == selected_district) & (df['A_NAME'] == selected_item)]
    summary_df = df_filtered.groupby('P_DATE')['A_PRICE'].mean().reset_index()
    summary_df = summary_df.rename(columns={'P_DATE': 'ds', 'A_PRICE': 'y'})

    model = Prophet()
    model.fit(summary_df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    csv = forecast.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button('결과 다운로드(CSV)', csv, f'{selected_district}_{selected_item}_예측_{periods}일간.csv', 'text/csv', key='download-csv')
    
    fig = plot_plotly(model, forecast)
    fig.update_layout(
        title=dict(text=f'{selected_district} {selected_item} 예측 {periods} 일간', font=dict(size=20), yref='paper'),
        xaxis_title='날짜',
        yaxis_title='가격(원)',
        autosize=False,
        width=700,
        height=800,
    )
    fig.update_yaxes(tickformat='000')
    st.plotly_chart(fig)




def run_ml(df):
    st.markdown("# 물가 예측 페이지 ")

    selected = option_menu(None, ['Home', '품목별', '자치구별', '보고서'],
                           icons=['house', 'bar-chart', 'file-spreadsheet', 'map'],
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
    elif selected == '품목별':
        predict_by_item(df)
    elif selected == '자치구별':
        predict_by_district(df)
    elif selected == '보고서':
        report_main(df)
    else:
        st.warning('Wrong')


