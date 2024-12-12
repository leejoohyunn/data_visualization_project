import streamlit as st

st.set_page_config(
    page_title="취업통계 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("취업통계 분석 대시보드 👋")

st.markdown("""
## 2023-2024 취업통계 분석
이 대시보드는 2023-2024년 취업통계 데이터를 분석하고 시각화한 결과를 제공합니다.

### 📊 제공 정보
1. **소개 페이지**: 전체 통계 요약
2. **교육정도별 취업자**: 교육수준별 분석
3. **지역별 취업자**: 지역 기반 분석
4. **종사상지위별 취업자**: 고용형태별 분석
5. **임금수준별 분석**: 임금 분포 분석
""")

# 핵심 지표
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("전체 취업자 수", "28,693명", "345명")
with col2:
    st.metric("전문가 비율", "21.9%", "0.4%")
with col3:
    st.metric("평균 임금대", "300~400만원", "상승")

