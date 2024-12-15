import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from pathlib import Path  # Path import 추가
import logging
import os

# 로깅 레벨 설정
logging.basicConfig(level=logging.DEBUG)
st.set_option('deprecation.showPyplotGlobalUse', False)

def load_data():
    # 데이터 생성
    data = {
        '지역': ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
                '경기', '강원', '충청북', '충청남', '전라북', '전라남', '경상북', '경상남', '제주'],
        '전체_취업자': [5252, 1688, 1227, 1682, 787, 792, 571, 210,
                    7713, 863, 968, 1280, 998, 1016, 1471, 1775, 400],
        '증감': [105, -7, -9, 35, 17, -2, -1, 1,
                103, 2, 19, 26, 18, -19, -21, -5, 2],
        '1위_직종': ['경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', 
                    '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직',
                    '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', 
                    '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', 
                    '농·축산 숙련직', '농·축산 숙련직', '농·축산 숙련직', '경영 및 회계 관련 사무직', 
                    '경영 및 회계 관련 사무직'],
        '1위_취업자': [897, 254, 172, 271, 125, 114, 75, 51,
                    1188, 101, 134, 184, 157, 183, 271, 249, 50],
        '1위_증감': [-1, 20, 12, 11, 10, -8, -1, 3,
                    8, -6, 19, 9, -5, -8, -19, 12, -1],
        '2위_직종': ['조리 및 음식 서비스직', '매장 판매 및 상품 대여직', '보건·사회복지 및 종교 관련직',
                    '청소 및 경비 관련 단순 노무직', '보건·사회복지 및 종교 관련직', '매장 판매 및 상품 대여직',
                    '기계 제조 및 관련 기계 조작직', '교육 전문가 및 관련직', '보건·사회복지 및 종교 관련직',
                    '농·축산 숙련직', '농·축산 숙련직', '농·축산 숙련직', '경영 및 회계 관련 사무직',
                    '경영 및 회계 관련 사무직', '경영 및 회계 관련 사무직', '농·축산 숙련직',
                    '농·축산 숙련직'],
        '2위_취업자': [366, 120, 98, 106, 54, 58, 48, 15,
                    440, 82, 107, 171, 119, 105, 173, 175, 42],
        '2위_증감': [43, -9, 8, 6, -2, 8, 1, 0,
                    -6, 7, 1, 7, 2, -5, 19, -18, -1],
        '3위_직종': ['문화·예술·스포츠 전문가 및 관련직', '조리 및 음식 서비스직', '교육 전문가 및 관련직',
                    '매장 판매 및 상품 대여직', '조리 및 음식 서비스직', '보건·사회복지 및 종교 관련직', '운전 및 운송 관련직',
                    '공학 전문가 및 기술직', '조리 및 음식 서비스직', '청소 및 경비비 관련 단순 노무직', '운전 및 운송 관련직',
                    '조리 및 음식 서비스직', '청소 및 경비 관련 단순 노무직', '청소 및 경비 관련 단순 노무직', '조리 및 음식 서비스직',
                    '청소 및 경비 관련 단순 노무직', '조리 및 음식 서비스직'],
        '3위_취업자': [340, 113, 73, 101, 52, 55, 35, 14,
                    433, 80, 62, 72, 72, 74, 93, 105, 33],
        '3위_증감': [43, -15, 5, 3, -6, -9, 4, 2,
                    37, -8, 5, -3, 5, -4, 7, 17, -2]
    }
    return pd.DataFrame(data)

def create_folium_map(df, geojson_data):
    # 중심 좌표를 한국 중앙으로 설정
    m = folium.Map(location=[36.0, 128.0], zoom_start=7)
    
    # Choropleth 생성
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=df,
        columns=['지역', '전체_취업자'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='전체 취업자 수 (천명)',
        highlight=True
    ).add_to(m)
    
    # 각 지역별 데이터를 GeoJSON에 추가
    for feature in choropleth.geojson.data['features']:
        region_name = feature['properties']['name']
        region_data = df[df['지역'] == region_name].iloc[0]
        
        feature['properties']['전체_취업자'] = f"{region_data['전체_취업자']:,}명"
        feature['properties']['1위_직종'] = region_data['1위_직종']
        feature['properties']['1위_취업자'] = f"{region_data['1위_취업자']:,}명"
        feature['properties']['2위_직종'] = region_data['2위_직종']
        feature['properties']['2위_취업자'] = f"{region_data['2위_취업자']:,}명"
        feature['properties']['3위_직종'] = region_data['3위_직종']
        feature['properties']['3위_취업자'] = f"{region_data['3위_취업자']:,}명"
    
    # Tooltip 추가
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', '전체_취업자',
                   '1위_직종', '1위_취업자',
                   '2위_직종', '2위_취업자',
                   '3위_직종', '3위_취업자'],
            aliases=['지역: ', '전체 취업자: ',
                    '1위 직종: ', '1위 취업자: ',
                    '2위 직종: ', '2위 취업자: ',
                    '3위 직종: ', '3위 취업자: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    
    return m

def main():
    st.set_page_config(
        layout="wide",
        page_title="지역별 취업자 현황",
        menu_items={
            'Get Help': 'https://www.streamlit.io/community',
            'Report a bug': "https://github.com/your-repo/issues",
            'About': "# 지역별 취업자 현황 분석 대시보드"
        }
    )
    st.title('지역별 직업종분류별 취업자 분석 대시보드')
    
    # 데이터 로드
    df = load_data()
    
    # 파일 경로 설정
    CURRENT_DIR = Path(__file__).parent.parent
    json_path = CURRENT_DIR / "assets" / "refined_korea1.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            geojson = json.load(f)
            st.write("GeoJSON 파일 로드 성공!")
            st.write("GeoJSON 데이터 크기:", len(str(geojson)), "bytes")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        st.write("현재 경로:", os.getcwd())
        st.write("파일 경로:", json_path)
        return
    # 탭 생성
    tab1, tab2 = st.tabs(['지도 기반 분석', '상세 분석'])
    
    with tab1:
        st.header('지역별 취업자 현황')
        
        # 시각화 선택 (Plotly vs Folium)
        map_type = st.radio("지도 유형 선택", ["인터랙티브 통계지도", "상세정보 지도"])
        
        if map_type == "인터랙티브 통계지도":
            # 기존 Plotly 지도
            viz_option = st.selectbox(
                '시각화 항목 선택',
                ['전체 취업자 수', '전체 증감']
            )
            
            if viz_option == '전체 취업자 수':
                choropleth_data = df['전체_취업자']
                title = '지역별 전체 취업자 수'
                colorscale = 'Viridis'
            else: 
                choropleth_data = df['증감']
                title = '지역별 전체 취업자 증감'
                colorscale = 'Viridis'


            fig = px.choropleth_mapbox(
                df,
                geojson=geojson,
                locations='지역',
                color=choropleth_data,
                featureidkey='properties.name',
                center={'lat': 36, 'lon': 127.5},
                zoom=5.5,
                mapbox_style='carto-positron',
                title=title,
                color_continuous_scale=colorscale,
                hover_data=['전체_취업자', '증감', '1위_취업자', '1위_증감']
            )
            
            fig.update_layout(
                height=800,  # 높이 증가
                width=1200,  # 너비 증가
                autosize=True,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            # Folium 지도
            st.write("각 지역을 클릭하면 상세 정보를 확인할 수 있습니다.")
            folium_map = create_folium_map(df, geojson)
            st_folium(folium_map, width=1000, height=600)

    # tab2의 내용은 그대로 유지
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('전체 취업자 수 상위 5개 지역')
            top_5_regions = df.nlargest(5, '전체_취업자')
            fig_top5 = px.bar(
                top_5_regions,
                x='지역',
                y='전체_취업자',
                text='전체_취업자',
                title='전체 취업자 수 상위 5개 지역',
                color='증감',
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_top5, use_container_width=True)
        
        with col2:
            st.subheader('지역별 증감 분포')
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=df['증감'],
                boxpoints='all',
                pointpos=-1.5,
                jitter=0.3,
                name='전체 증감'
            ))
            fig_box.add_trace(go.Box(
                y=df['1위_증감'],
                boxpoints='all',
                pointpos=-1.5,
                jitter=0.3,
                name='1위 직종 증감'
            ))
            st.plotly_chart(fig_box, use_container_width=True)

        st.subheader('전체 취업자 수와 증감의 관계')
        fig_scatter = px.scatter(
            df,
            x='전체_취업자',
            y='증감',
            text='지역',
            title='전체 취업자 수와 증감의 관계',
            trendline='ols',
            trendline_color_override='red'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader('지역별 증감 순위')
        fig_rank = px.bar(
            df.sort_values('증감', ascending=True),
            x='지역',
            y='증감',
            title='지역별 증감 순위',
            color='증감',
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_rank, use_container_width=True)

if __name__ == "__main__":
    main()
