# pages/4_종사상지위별_취업자.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="종사상지위별 취업자", layout="wide")

st.title("종사상지위별 취업자 분석")

# 설명
st.markdown("""
### 종사상지위 구분
- **임금근로자**: 고용주와 고용계약을 맺고 일하는 근로자
- **상용근로자**: 1년 이상의 고용계약을 맺은 정규직 근로자
- **임시·일용직**: 1년 미만의 계약직 또는 일용직 근로자
- **비임금근로자**: 자영업자 및 무급가족종사자
""")

# 데이터 준비
status_data = pd.DataFrame({
    '지위': ['임금근로자', '상용', '임시·일용', '비임금근로자'],
    '인원': [22139, 16398, 5741, 6555],
    '비율': [77.2, 57.1, 20.1, 22.8]
})

# 전체 분포
fig1 = px.pie(status_data, values='인원', names='지위',
              title='종사상지위별 취업자 분포')
st.plotly_chart(fig1)

# 임금근로자 세부분석
st.subheader("임금근로자 세부 분석")
wage_workers = pd.DataFrame({
    '구분': ['상용', '임시·일용'],
    '인원': [16398, 5741],
    '비율': [74.1, 25.9]
})
fig2 = px.pie(wage_workers, values='인원', names='구분',
              title='임금근로자 구성비')
st.plotly_chart(fig2)
