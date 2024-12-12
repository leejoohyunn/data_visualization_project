# pages/3_지역별_취업자.py
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="지역별 취업자", layout="wide")

st.title("지역별 취업자 분석")

# 데이터 준비
regional_data = pd.DataFrame({
    '지역': ['서울', '부산', '대구', '인천', '광주', '대전', '울산'],
    '취업자수': [5252, 1688, 1227, 1682, 787, 792, 571],
    '1순위': ['경영관리', '경영관리', '경영관리', '경영관리', '경영관리', '경영관리', '경영관리'],
    '2순위': ['서비스', '판매', '교육', '서비스', '서비스', '교육', '서비스'],
    '3순위': ['교육', '서비스', '서비스', '판매', '판매', '서비스', '판매'],
    'lat': [37.5665, 35.1796, 35.8714, 37.4563, 35.1595, 36.3504, 35.5384],
    'lon': [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114]
})

# 지도 시각화
st.subheader("지역별 취업자 분포")
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for idx, row in regional_data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['취업자수']/100,
        popup=f"{row['지역']}<br>취업자수: {row['취업자수']}<br>1순위: {row['1순위']}<br>2순위: {row['2순위']}<br>3순위: {row['3순위']}",
        color='red',
        fill=True
    ).add_to(m)

folium_static(m)

# 순위별 분석
st.subheader("지역별 주요 직종 현황")
for rank in ['1순위', '2순위', '3순위']:
    fig = px.bar(regional_data, x='지역', y='취업자수', color=rank,
                 title=f'지역별 {rank} 직종 분포')
    st.plotly_chart(fig)

