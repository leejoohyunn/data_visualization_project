import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    st.subheader("2023년 임금수준별 분포")
    fig1 = px.pie(salary_data, values='2023', names='임금구간',
                  title='2023년 임금수준별 분포')
    st.plotly_chart(fig1)

with col2:
    st.subheader("2024년 임금수준별 분포")
    fig2 = px.pie(salary_data, values='2024', names='임금구간',
                  title='2024년 임금수준별 분포')
    st.plotly_chart(fig2)

# 증감 분석
st.subheader("2023-2024 임금수준별 증감")
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=salary_data['임금구간'],
    y=salary_data['증감'],
    marker_color=['red' if x < 0 else 'blue' for x in salary_data['증감']]
))
fig3.update_layout(title='임금수준별 증감률 (%p)',
                  yaxis_title='증감률')
st.plotly_chart(fig3)

# 직종별 임금수준 분석
occupation_salary = pd.DataFrame({
    '직종': ['전문가', '사무', '서비스', '판매', '기능원'],
    '평균임금': [350, 280, 220, 200, 260],
    '중위임금': [320, 260, 200, 180, 240]
})

st.subheader("직종별 임금 수준")
fig4 = go.Figure()
fig4.add_trace(go.Bar(name='평균임금', x=occupation_salary['직종'], 
                      y=occupation_salary['평균임금']))
fig4.add_trace(go.Bar(name='중위임금', x=occupation_salary['직종'], 
                      y=occupation_salary['중위임금']))
fig4.update_layout(barmode='group', title='직종별 평균/중위 임금')
st.plotly_chart(fig4)

# 통계 요약
st.subheader("주요 특징")
col1, col2 = st.columns(2)
with col1:
    st.metric("중위임금 구간", "200~300만원", "-1.6%p")
    st.metric("최다 증가 구간", "400만원 이상", "+1.9%p")
with col2:
    st.metric("최소임금 구간 비율", "9.4%", "+0.3%p")
    st.metric("최다 감소 구간", "200~300만원", "-1.6%p")

# 임금 구간별 추세 분석
st.subheader("임금 구간별 추세")
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=['2023', '2024'], y=[salary_data.iloc[0]['2023'], 
                                                salary_data.iloc[0]['2024']],
                         mode='lines+markers', name='100만원 미만'))
fig5.add_trace(go.Scatter(x=['2023', '2024'], y=[salary_data.iloc[-1]['2023'], 
                                                salary_data.iloc[-1]['2024']],
                         mode='lines+markers', name='400만원 이상'))
fig5.update_layout(title='주요 임금구간 추세 변화',
                  yaxis_title='비율(%)')
st.plotly_chart(fig5)
