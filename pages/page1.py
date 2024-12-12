# pages/1_소개페이지.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="소개 페이지", layout="wide")

st.title("취업통계 종합 현황")

# 5개 주요 지표 탭
tabs = st.tabs(["지역별", "교육정도별", "종사상지위별", "임금수준별", "교육분류별"])

with tabs[0]:
    st.header("지역별 취업자 현황")
    regional_data = pd.DataFrame({
        '지역': ['서울', '부산', '대구', '인천', '광주', '대전', '울산'],
        '취업자수': [5252, 1688, 1227, 1682, 787, 792, 571]
    })
    fig = px.bar(regional_data, x='지역', y='취업자수',
                 title='지역별 취업자 분포')
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.header("교육정도별 취업자 현황")
    education_data = pd.DataFrame({
        '교육정도': ['전체', '중졸이하', '고졸', '대졸'],
        '비율': [100, 22.3, 21.4, 17.6]
    })
    fig = px.pie(education_data, values='비율', names='교육정도',
                 title='교육정도별 취업자 분포')
    st.plotly_chart(fig, use_container_width=True)
