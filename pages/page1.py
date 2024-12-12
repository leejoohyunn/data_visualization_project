import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="소개 페이지", layout="wide")

st.title("취업통계 종합 현황")

# 5가지 주요 통계 데이터 표시
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

with tabs[2]:
    st.header("종사상지위별 취업자 현황")
    status_data = pd.DataFrame({
        '지위': ['임금근로자', '상용', '임시·일용', '비임금근로자'],
        '비율': [77.2, 57.1, 20.1, 22.8]
    })
    fig = px.pie(status_data, values='비율', names='지위',
                 title='종사상지위별 취업자 분포')
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.header("임금수준별 근로자 현황")
    salary_data = pd.DataFrame({
        '임금구간': ['100만원 미만', '100~200만원', '200~300만원', '300~400만원', '400만원 이상'],
        '비율': [9.4, 10.7, 32.1, 21.9, 25.9]
    })
    fig = px.bar(salary_data, x='임금구간', y='비율',
                 title='임금수준별 근로자 분포')
    st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.header("교육분류별 취업자 현황")
    edu_cat_data = pd.DataFrame({
        '교육분류': ['전체', '교육', '예술', '인문학', '사회'],
        '취업자수': [14977, 1066, 926, 1209, 632]
    })
    fig = px.bar(edu_cat_data, x='교육분류', y='취업자수',
                 title='교육분류별 취업자 분포')
    st.plotly_chart(fig, use_container_width=True)
