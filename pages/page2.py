# pages/2_교육정도별_취업자.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="교육정도별 취업자", layout="wide")

st.title("교육정도별 취업자 분석")

# 데이터 준비
education_data = pd.DataFrame({
    '직업중분류': ['청소 및 경비 관련', '농축산 숙련직', '조리 및 음식 서비스직', '물류 보건', '운전 및 운송'],
    '2023상반기': [785, 817, 238, 214, 208],
    '2024상반기': [790, 783, 225, 213, 200],
    '증감': [5, -34, -13, -1, -8]
})

# 연도별 비교
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(education_data, values='2023상반기', names='직업중분류',
                  title='2023년 상반기 직업별 분포')
    st.plotly_chart(fig1)

with col2:
    fig2 = px.pie(education_data, values='2024상반기', names='직업중분류',
                  title='2024년 상반기 직업별 분포')
    st.plotly_chart(fig2)

# 증감 분석
fig3 = px.bar(education_data, x='직업중분류', y='증감',
              title='2023-2024 증감 현황',
              color='증감',
              color_continuous_scale=['red', 'blue'])
st.plotly_chart(fig3)

# 상하위 3개 분야 분석
st.subheader("주요 증감 현황")
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 상위 증가 분야")
    top_increase = education_data.nlargest(3, '증감')
    st.dataframe(top_increase[['직업중분류', '증감']])
with col2:
    st.markdown("#### 상위 감소 분야")
    top_decrease = education_data.nsmallest(3, '증감')
    st.dataframe(top_decrease[['직업중분류', '증감']])

