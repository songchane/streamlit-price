import streamlit as st
import pandas as pd
import plotly.express as px

def donut_chart_analysis(total_df):
    st.markdown('# 요소 분석')
    st.markdown("- 각 품목이 자치구 전체 평균 가격에서 차지하는 비율을 한눈에 파악 \n"
                "- 각 품목의 평균 가격과 해당 품목의 비율을 동시에 확인 \n"
                "- 사용자에게 데이터를 더 잘 전달하고 이해시키는 데 도움이 됩니다. 직관적인 디자인으로 데이터를 쉽게 인식")

    # 자치구명 선택
    sgg_nm = st.sidebar.selectbox('자치구 선택', total_df['M_GU_NAME'].unique(), key='select_borough_donut')
    
    # Filter data for selected borough
    filtered_df = total_df[total_df['M_GU_NAME'] == sgg_nm]

    # Calculate average price by item
    avg_price_by_item = filtered_df.groupby('A_NAME')['A_PRICE'].mean().reset_index()

    # Create donut chart
    fig = px.pie(avg_price_by_item, values='A_PRICE', names='A_NAME', title=f'{sgg_nm} 평균 물가 가격 요소 비율',
                 hole=0.4, labels={'A_PRICE': 'Average Price', 'A_NAME': 'Item'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True)
    
    st.plotly_chart(fig, use_container_width=True)

def run_donut(total_df):
    total_df['P_DATE'] = pd.to_datetime(total_df['P_DATE'], format='%Y-%m-%d')

    # 도넛 차트 분석 수행
    donut_chart_analysis(total_df)