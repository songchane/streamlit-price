import streamlit as st
import pandas as pd
from pingouin import ttest
import plotly.express as px

def correlation_analysis(total_df, sgg_nm1, sgg_nm2, a_name):
    st.markdown(f'#### {sgg_nm1}와 {sgg_nm2}의 {a_name} 월별 평균 가격 상관관계 분석')

    # 선택한 자치구와 품목으로 데이터 필터링
    filtered_df1 = total_df[(total_df['M_GU_NAME'] == sgg_nm1) & (total_df['A_NAME'] == a_name)]
    filtered_df2 = total_df[(total_df['M_GU_NAME'] == sgg_nm2) & (total_df['A_NAME'] == a_name)] 

    # 월별 평균 가격 계산
    avg_price_df1 = filtered_df1.groupby(filtered_df1['P_DATE'].dt.month)['A_PRICE'].mean().reset_index()
    avg_price_df2 = filtered_df2.groupby(filtered_df2['P_DATE'].dt.month)['A_PRICE'].mean().reset_index()

    # 두 자치구의 월별 평균 가격을 합칩니다.
    merged_df = pd.merge(avg_price_df1, avg_price_df2, on='P_DATE', suffixes=('_' + sgg_nm1, '_' + sgg_nm2))

    # 상관계수 계산
    corr_coef = merged_df[['A_PRICE_' + sgg_nm1, 'A_PRICE_' + sgg_nm2]].corr().iloc[0, 1]
    st.write(f'상관계수: {corr_coef:.2f}')

    # t-검정 수행
    ttest_result = ttest(filtered_df1['A_PRICE'], filtered_df2['A_PRICE'], paired=False)
    
    # 결과 출력
    st.dataframe(ttest_result, use_container_width=True)

    # 상관관계 설명
    if corr_coef > 0.5:
        st.markdown(f'''
            <div style="border: 2px solid #778da9; padding: 10px; border-radius: 10px;">
                <h3 style="color: black;"><b>상관계수가 0.5보다 큽니다.</b></h3>
                <h5 style="color: black;">{sgg_nm1}과 {sgg_nm2}의 {a_name} 월별 평균 가격은 양의 상관관계를 가집니다.</h5>
            </div>
        ''', unsafe_allow_html=True)
    elif corr_coef < -0.5:
        st.markdown(f'''
            <div style="border: 2px solid #778da9; padding: 10px; border-radius: 10px;">
                <h3 style="color: black;"><b>상관계수가 -0.5보다 작습니다.</b></h3>
                <h5 style="color: black;">{sgg_nm1}과 {sgg_nm2}의 {a_name} 월별 평균 가격은 음의 상관관계를 가집니다.</h5>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div style="border: 2px solid #778da9; padding: 10px; border-radius: 10px;">
                <h3 style="color: black;"><b>상관계수가 -0.5 ~ 0.5 사이입니다.</b></h3>
                <h5 style="color: black;">{sgg_nm1}과 {sgg_nm2}의 {a_name} 월별 평균 가격은 관련성이 낮습니다.</h5>
            </div>
        ''', unsafe_allow_html=True)



def showStat(total_df):
    total_df['P_DATE'] = pd.to_datetime(total_df['P_DATE'], format='%Y-%m-%d')

    # 자치구명 선택
    sgg_nm1 = st.sidebar.selectbox('첫 번째 자치구명', total_df['M_GU_NAME'].unique())
    sgg_nm2 = st.sidebar.selectbox('두 번째 자치구명', total_df['M_GU_NAME'].unique())
    
    # 품목 선택
    a_name = st.sidebar.selectbox('품목 선택', total_df['A_NAME'].unique())

    # 두 자치구가 다른 경우에만 분석을 수행합니다.
    if sgg_nm1 != sgg_nm2:
        # 상관관계 분석
        correlation_analysis(total_df, sgg_nm1, sgg_nm2, a_name)
    else:
        st.warning('두 자치구가 동일합니다. 다른 자치구를 선택하세요.')
