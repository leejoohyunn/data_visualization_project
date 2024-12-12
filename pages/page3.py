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
    '1순위': ['경영 및 회계', '조리 및 음식', '경영 및 회계', '경영 및 회계', '경영 및 회계', '경영 및 회계', '경영 및 회계'],
    '2순위': ['서비스', '판매', '교육', '서비스', '서비스', '교육', '서비스'],
    '3순위': ['교육', '서비스', '서비스', '판매', '판매', '서비스', '판매'],
    'lat': [37.5665, 35.1796, 35.8714, 37.4563, 35.1595, 36.3504, 35.5384],
    'lon': [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114]
})

# 지도 시각화
st.subheader("지역별 취업자 분포 지도")
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for idx, row in regional_data.iterrows():
    popup_content = f"""
        <div style='width: 200px'>
            <b>{row['지역']}</b><br>
            취업자수: {row['취업자수']}명<br>
            1순위: {row['1순위']}<br>
            2순위: {row['2순위']}<br>
            3순위: {row['3순위']}
        </div>
    """
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['취업자수']/100,
        popup=folium.Popup(popup_content, max_width=300),
        color='red',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

folium_static(m)

# 지역별 취업자 수 비교
st.subheader("지역별 취업자 수 비교")
fig1 = px.bar(regional_data, x='지역', y='취업자수',
              title='지역별 취업자 수',
              color='취업자수',
              color_continuous_scale='Viridis')
st.plotly_chart(fig1)

# 지역별 상위 직종 분석
st.subheader("지역별 상위 직종 분포")
rankings = pd.melt(regional_data, 
                  id_vars=['지역', '취업자수'],
                  value_vars=['1순위', '2순위', '3순위'],
                  var_name='순위',
                  value_name='직종')

fig2 = px.bar(rankings, x='지역', y='취업자수', color='직종',
              title='지역별 상위 직종 분포',
              barmode='group')
st.plotly_chart(fig2)

# 지역별 세부 정보
st.subheader("지역별 세부 정보")
for city in regional_data['지역'].unique():
    with st.expander(f"{city} 세부 정보"):
        city_data = regional_data[regional_data['지역'] == city].iloc[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("취업자 수", f"{city_data['취업자수']:,}명")
        with col2:
            st.write("상위 직종:")
            st.write(f"1순위: {city_data['1순위']}")
            st.write(f"2순위: {city_data['2순위']}")
        with col3:
            st.write("비중:")
            total = regional_data['취업자수'].sum()
            st.write(f"전체 대비: {(city_data['취업자수']/total*100):.1f}%")
