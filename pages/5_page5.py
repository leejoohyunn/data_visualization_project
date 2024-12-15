import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

def load_data():
    # 교육분야별 취업자 데이터
    data = {
        '교육분류': ['교육', '예술', '인문학', '사회', '경영', '자연', '정보', '공학', '농업', '보건', '복지', '서비스'],
        '전체취업자': [1066, 1166, 1209, 632, 2493, 628, 546, 4130, 192, 1183, 639, 1095],
        '증감': [6, 60, 35, 42, 44, -10, -11, 204, -1, 42, 43, 49],
        '비율': [7.1, 7.8, 8.1, 4.2, 16.6, 4.2, 3.6, 27.6, 1.3, 7.9, 4.3, 7.3],
        '1순위_직업': ['전문가 및 관련종사자', '전문가 및 관련종사자', '전문가 및 관련종사자', 
                   '사무종사자', '사무종사자', '전문가 및 관련종사자', '전문가 및 관련종사자',
                   '전문가 및 관련종사자', '사무종사자', '전문가 및 관련종사자', 
                   '전문가 및 관련종사자', '서비스종사자'],
        '1순위_비율': [62.5, 47.9, 34.8, 39.4, 43.5, 42.9, 36.8, 36.6, 24.0, 72.8, 39.5, 27.6],
        '2순위_직업': ['사무종사자', '사무종사자', '사무종사자', '전문가 및 관련종사자',
                   '전문가 및 관련종사자', '사무종사자', '사무종사자', '사무종사자',
                   '전문가 및 관련종사자', '사무종사자', '사무종사자', '사무종사자'],
        '2순위_비율': [12.7, 16.8, 31.4, 30.1, 18.8, 27.9, 24.9, 21.5, 19.8, 11.5, 24.9, 21.3],
        '3순위_직업': ['서비스종사자', '판매종사자', '서비스종사자', '서비스종사자',
                   '판매종사자', '서비스종사자', '장치기계조작', '장치기계조작',
                   '농림어업숙련', '서비스종사자', '서비스종사자', '전문가및관련종사자'],
        '3순위_비율': [8.2, 11.5, 9.7, 6.9, 9.3, 6.4, 8.2, 12.0, 16.3, 5.4, 13.0, 19.2]
    }
    return pd.DataFrame(data)

def create_sunburst_chart(df):
    # 데이터 준비
    sunburst_data = []
    for _, row in df.iterrows():
        # 1순위 직업
        sunburst_data.append({
            '교육분류': row['교육분류'],
            '직업순위': '1순위',
            '직업': row['1순위_직업'],
            '비율': row['1순위_비율']
        })
        # 2순위 직업
        sunburst_data.append({
            '교육분류': row['교육분류'],
            '직업순위': '2순위',
            '직업': row['2순위_직업'],
            '비율': row['2순위_비율']
        })
        # 3순위 직업
        sunburst_data.append({
            '교육분류': row['교육분류'],
            '직업순위': '3순위',
            '직업': row['3순위_직업'],
            '비율': row['3순위_비율']
        })
    
    sunburst_df = pd.DataFrame(sunburst_data)
    fig = px.sunburst(sunburst_df,
                      path=['교육분류', '직업순위', '직업'],
                      values='비율',
                      color='비율',
                      color_continuous_scale='Viridis',
                      title='교육분류별 직업 분포 계층구조')
    return fig

def main():
    st.set_page_config(layout="wide", page_title="교육분류별 취업자 분석")
    
    # 커스텀 CSS 추가
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            padding-bottom: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title('교육분류별 취업자 현황 종합 분석')
    
    df = load_data()
    
    # 핵심 지표 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 취업자 수", f"{df['전체취업자'].sum():,}명",
                 f"{df['증감'].sum():+}명")
    with col2:
        st.metric("최다 취업 분야", "공학",
                 f"비율 {df[df['교육분류']=='공학']['비율'].values[0]}%")
    with col3:
        st.metric("최다 증가 분야", "공학",
                 f"+{df[df['교육분류']=='공학']['증감'].values[0]}명")
    with col4:
        top_job = df['1순위_직업'].mode().values[0]
        st.metric("가장 흔한 취업 직군", top_job)
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(['종합 현황', '직업 분포', '상세 분석'])
    
    # 탭 1: 종합 현황
    with tab1:
        st.header('교육분류별 종합 현황')
        
        # 복합 차트 (취업자 수 + 증감률)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(name='취업자 수', x=df['교육분류'], y=df['전체취업자'],
                  text=df['전체취업자'], textposition='outside'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(name='증감', x=df['교육분류'], y=df['증감'],
                      mode='lines+markers+text', text=df['증감'],
                      textposition='top center', line=dict(color='red')),
            secondary_y=True
        )
        
        fig.update_layout(
            title='교육분류별 취업자 수 및 증감 추이',
            barmode='group',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 비율 분포 워터폴 차트
        fig_waterfall = go.Figure(go.Waterfall(
            name="비율",
            orientation="v",
            measure=["relative"] * len(df),
            x=df['교육분류'],
            textposition="outside",
            text=df['비율'].round(1).astype(str) + '%',
            y=df['비율'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig_waterfall.update_layout(
            title="교육분류별 취업자 비율 분포",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_waterfall, use_container_width=True)

    # 탭 2: 직업 분포
    with tab2:
        st.header('교육분류별 직업 분포 분석')
        
        # 선버스트 차트
        fig_sunburst = create_sunburst_chart(df)
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # 직업별 히트맵
        st.subheader('직업 순위별 분포 히트맵')
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df[['1순위_비율', '2순위_비율', '3순위_비율']].values,
            x=['1순위', '2순위', '3순위'],
            y=df['교육분류'],
            colorscale='Viridis',
            text=df[['1순위_비율', '2순위_비율', '3순위_비율']].values.round(1),
            texttemplate='%{text}%',
            textfont={"size": 10}
        ))
        
        fig_heatmap.update_layout(
            title='교육분류별 직업 순위 분포',
            height=600
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # 탭 3: 심층 분석
    with tab3:
        st.header('교육분류별 심층 분석')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 상위 직종 집중도
            df['직종집중도'] = df['1순위_비율'] + df['2순위_비율']
            fig_concentration = px.scatter(df,
                                        x='전체취업자',
                                        y='직종집중도',
                                        size='비율',
                                        color='증감',
                                        text='교육분류',
                                        title='취업자 규모 vs 직종 집중도',
                                        labels={'전체취업자': '전체 취업자 수',
                                               '직종집중도': '상위 2개 직종 비율 합계(%)'})
            
            fig_concentration.update_traces(textposition='top center')
            st.plotly_chart(fig_concentration, use_container_width=True)
        
        with col2:
            # 직업 다양성 지수
            df['직업다양성'] = (100 - df['1순위_비율']) / 100
            fig_diversity = px.bar(df,
                                 x='교육분류',
                                 y='직업다양성',
                                 color='직업다양성',
                                 title='직업 다양성 지수 (높을수록 다양)',
                                 labels={'직업다양성': '직업 다양성 지수'})
            
            st.plotly_chart(fig_diversity, use_container_width=True)
        
        # 군집 분석 결과
        st.subheader('교육분류 유형 분석')
        cluster_cols = ['전체취업자', '직종집중도', '직업다양성', '증감']
        scaled_data = (df[cluster_cols] - df[cluster_cols].mean()) / df[cluster_cols].std()
        
        fig_parallel = go.Figure(data=
            go.Parcoords(
                line=dict(color=df['비율'],
                         colorscale='Viridis'),
                dimensions=[
                    dict(range=[df['전체취업자'].min(), df['전체취업자'].max()],
                         label='취업자 수', values=df['전체취업자']),
                    dict(range=[df['직종집중도'].min(), df['직종집중도'].max()],
                         label='직종집중도', values=df['직종집중도']),
                    dict(range=[df['직업다양성'].min(), df['직업다양성'].max()],
                         label='직업다양성', values=df['직업다양성']),
                    dict(range=[df['증감'].min(), df['증감'].max()],
                         label='증감', values=df['증감'])
                ]
            )
        )
        
        fig_parallel.update_layout(title='교육분류별 특성 패턴 분석')
        st.plotly_chart(fig_parallel, use_container_width=True)

        st.info("""
        ### 주요 발견점
        1. 공학계열의 높은 취업 비중
        2. 직업 선택의 전공-직무 불일치 현상 (인문학, 예술 분야에서 불일치 현상 두드러짐)
        3. 보건 분야의 높은 전공 연계성
        4. 교육분류별 고용 안정성 차이 (산업 구조 변화와 노동시장 수요 변화가 반영됐음을 시사)
        """)
if __name__ == "__main__":
    main()
