import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="종사상지위별 취업자", layout="wide")

st.title("종사상지위별 취업자 분석")

# 취업자 정의 설명
st.markdown("""
### 📌 취업자 구분
1. **임금근로자**
   - 고용주와 명시적/암묵적 고용계약을 체결하고 일하는 근로자
   - 상용근로자와 임시·일용근로자로 구분

2. **비임금근로자**
   - 자영업자: 자기 책임 하에 독립적으로 사업을 영위하는 자
   - 무급가족종사자: 가족이 운영하는 사업체에서 무보수로 일하는 자
""")

# 데이터 준비
status_data = pd.DataFrame({
    '지위': ['임금근로자', '상용', '임시·일용', '비임금근로자'],
    '인원': [22139, 16398, 5741, 6555],
    '비율': [77.2, 57.1, 20.1, 22.8]
})

# 전체 분포 시각화
st.subheader("취업자 종사상지위 분포")
fig1 = px.pie(status_data, values='인원', names='지위',
              title='종사상지위별 취업자 분포',
              hole=0.4)
st.plotly_chart(fig1)

# 임금근로자 세부 분석
wage_workers = pd.DataFrame({
    '구분': ['상용', '임시·일용'],
    '인원': [16398, 5741],
    '비율': [74.1, 25.9]
})

col1, col2 = st.columns(2)
with col1:
    st.subheader("임금근로자 구성")
    fig2 = px.pie(wage_workers, values='인원', names='구분',
                  title='임금근로자 구성비')
    st.plotly_chart(fig2)

# 직종별 종사상지위 분포
occupation_status = pd.DataFrame({
    '직종': ['전문가', '사무', '서비스', '판매', '기능원'],
    '상용': [80, 75, 60, 55, 70],
    '임시·일용': [20, 25, 40, 45, 30]
})

with col2:
    st.subheader("주요 직종별 고용형태")
    fig3 = go.Figure(data=[
        go.Bar(name='상용', x=occupation_status['직종'], y=occupation_status['상용']),
        go.Bar(name='임시·일용', x=occupation_status['직종'], y=occupation_status['임시·일용'])
    ])
    fig3.update_layout(barmode='stack', title='직종별 고용형태 비율')
    st.plotly_chart(fig3)

# 통계 요약
st.subheader("주요 통계")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("전체 취업자", f"{sum(status_data['인원']):,}명")
with col2:
    st.metric("임금근로자 비율", f"{status_data.iloc[0]['비율']}%")
with col3:
    st.metric("상용직 비율", f"{wage_workers.iloc[0]['비율']}%")
with col4:
    st.metric("임시·일용직 비율", f"{wage_workers.iloc[1]['비율']}%")
