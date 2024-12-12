# pages/5_임금수준별_근로자.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="임금수준별 근로자", layout="wide")

st.title("임금수준별 임금근로자 분석")

# 데이터 준비
salary_data = pd.DataFrame({
    '임금구간': ['100만원 미만', '100~200만원', '200~300만원', '300~400만원', '400만원 이상'],
    '2023': [9.1, 11.9, 33.7, 21.3, 24.0],
    '2024': [9.4, 10.7, 32.1, 21.9, 25.9],
    '증감': [0.3, -1.2, -1.6, 0.6, 1.9]
})

# 연도별 비교
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(salary_data, values='2023', names='임금구간',
                  title='2023년 임금수준별 분포')
    st.plotly_chart(fig1)

with col2:
    fig2 = px.pie(salary_data, values='2024', names='임금구간',
                  title='2024년 임금수준별 분포')
    st.plotly_chart(fig2)

# 증감 분석
fig3 = px.bar(salary_data, x='임금구간', y='증감',
              title='임금수준별 증감률 (2023-2024)',
              color='증감',
              color_continuous_scale=['red', 'blue'])
st.plotly_chart(fig3)

# 통계 요약
st.subheader("주요 특징")
col1, col2 = st.columns(2)
with col1:
    st.metric("중위임금 구간", "200~300만원", "-1.6%")
    st.metric("최다 증가 구간", "400만원 이상", "+1.9%")
with col2:
    st.metric("최소임금 구간 비율", "9.4%", "+0.3%")
    st.metric("최다 감소 구간", "200~300만원", "-1.6%")
