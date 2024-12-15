import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="취업 동향 종합 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# 페이지 타이틀과 설명
st.title("📊 취업 동향 종합 분석 대시보드")
st.markdown("""
### 2024년 상반기 취업 시장 동향 분석
이 대시보드는 다양한 관점에서 취업 시장의 현황과 변화를 분석합니다:

#### 📑 분석 페이지 구성
1. **교육정도별 취업자 분석**
   - 교육 수준에 따른 취업자 분포와 변화 추이
   - 교육정도별 주요 직종 분석

5. **지역별 취업자 분석**
   - 지역별 취업자 현황 및 변화
   - 지역별 주요 직종 분석

2. **종사상지위별 직업 분석**
   - 직업별 고용형태 분포
   - 고용 안정성 및 상관관계 분석

3. **직업대분류별 임금 분포 현황 대시보드**
   - 직종별 임금 수준 및 분포
   - 고임금/저임금 직종 분석

5. **교육분류별 취업자 분석**
   - 전공별 취업 현황 및 증감
   - 교육분류별 주요 직종 분포


""")

# 분석 주요 발견점
st.header("🔍 주요 분석 결과")

st.markdown("""
### 1. 교육 수준별 특징
- 대졸 이상 취업자의 지속적 증가 추세
- 중졸 이하 취업자는 단순노무 및 서비스직 집중
- 고졸 취업자는 사무/서비스/판매직 중심

### 2. 고용 형태 트렌드
- 정규직 비중 상승 지속
- 임시일용직은 서비스업 중심으로 분포
- 비임금근로자는 농림어업과 자영업 중심

### 3. 임금 수준 변화
- 전문직과 관리직의 고임금 비중 증가
- 서비스/판매직의 임금 격차 지속
- IT/금융 분야의 임금 상승세

### 4. 지역별 특성
- 수도권 중심의 취업자 증가
- 지방 대도시의 제조업 취업자 감소
- 농어촌 지역의 고령화 영향 뚜렷
""")

# 데이터 관련 참고사항
st.sidebar.header("📌 데이터 참고사항")
st.sidebar.markdown("""
- 데이터 출처: 통계청 경제활동인구조사
- 기준시점: 2024년 상반기
- 갱신주기: 반기별
""")

# 사이드바에 페이지 설명
st.sidebar.header("🔎 페이지 상세 설명")
st.sidebar.markdown("""
**1. 교육정도별 분석**
- 교육 수준별 취업자 현황
- 교육별 주요 직종 분포
- 전년 대비 변화 분석

**2. 지역별 분석**
- 지역별 취업자 현황
- 지역별 주요 직종
- 지역 간 격차 분석

**3. 종사상지위별 분석**
- 고용형태별 분포
- 직종별 고용 안정성
- 고용형태 간 상관관계

**4. 임금 분포 분석**
- 직종별 임금 수준
- 임금 구간별 분포
- 저임금/고임금 직종 분석

**5. 교육분류별 분석**
- 전공별 취업자 현황
- 전공-직종 매칭 분석
- 전공별 취업 트렌드


""")

# 푸터 정보
st.markdown("""
---
홍익대학교 산업데이터공학과 이주현
""")
