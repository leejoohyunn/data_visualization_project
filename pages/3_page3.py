import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

def load_data():
    data = {
        '직업대분류': ['관리자', '전문가 및 관련 종사자', '사무 종사자', '서비스 종사자', 
                    '판매 종사자', '농림·어업 숙련 종사자', '기능원 및 관련 기능 종사자',
                    '장치·기계 조작 및 조립 종사자', '단순노무 종사자'],
        '취업자': [1.5, 21.9, 17.6, 12.3, 8.7, 5.3, 8.0, 10.6, 14.1],
        '임금근로자': [1.9, 24.2, 21.6, 11.3, 6.6, 0.3, 7.7, 9.9, 16.7],
        '상용': [2.5, 29.4, 27.2, 8.9, 5.0, 0.2, 7.1, 11.9, 7.8],
        '임시일용': [0.0, 9.4, 5.6, 18.1, 11.1, 0.4, 9.3, 4.1, 42.0],
        '비임금근로자': [0.3, 14.3, 4.1, 15.6, 16.1, 22.2, 9.1, 12.9, 5.4]
    }
    df = pd.DataFrame(data)
    
    # 추가 계산
    df['임금근로자_비율'] = df['임금근로자'] / df['취업자'] * 100
    df['상용직_비율'] = df['상용'] / df['임금근로자'] * 100
    df['고용안정성_지수'] = (df['상용'] * 1 + df['임시일용'] * 0.5) / df['임금근로자'] * 100
    
    return df

def create_job_distribution_chart(df):
    # 직업별 고용형태 분포
    fig = go.Figure()
    
    # 스택 바 차트 추가
    fig.add_trace(
        go.Bar(name='상용', x=df['직업대분류'], y=df['상용'],
               marker_color='rgb(55, 83, 109)')
    )
    fig.add_trace(
        go.Bar(name='임시일용', x=df['직업대분류'], y=df['임시일용'],
               marker_color='rgb(26, 118, 255)')
    )
    fig.add_trace(
        go.Bar(name='비임금근로자', x=df['직업대분류'], y=df['비임금근로자'],
               marker_color='rgb(128, 128, 128)')
    )
    
    fig.update_layout(
        barmode='stack',
        title='직업별 고용형태 분포',
        xaxis_title='직업대분류',
        yaxis_title='비율 (%)',
        height=600
    )
    
    return fig

def create_employment_analysis(df):
    # 고용형태별 상관관계 분석
    correlation_matrix = df[['임금근로자', '상용', '임시일용', '비임금근로자']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=['임금근로자', '상용', '임시일용', '비임금근로자'],
        y=['임금근로자', '상용', '임시일용', '비임금근로자'],
        colorscale='RdBu',
        zmin=-1, zmax=1
    ))
    
    fig.update_layout(
        title='고용형태간 상관관계 분석',
        height=500
    )
    return fig

def create_stability_chart(df):
    fig = go.Figure()
    
    # 고용안정성 지수 추가
    fig.add_trace(
        go.Bar(
            name='고용안정성 지수',
            x=df['직업대분류'],
            y=df['고용안정성_지수'],
            marker_color='rgb(158,202,225)'
        )
    )
    
    # 상용직 비율 추가
    fig.add_trace(
        go.Scatter(
            name='상용직 비율',
            x=df['직업대분류'],
            y=df['상용직_비율'],
            mode='lines+markers',
            line=dict(color='red', width=2)
        )
    )
    
    fig.update_layout(
        title='직업별 고용 안정성 분석',
        xaxis_title='직업대분류',
        yaxis_title='비율 (%)',
        height=500,
        showlegend=True
    )
    
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title('💼 종사상지위별 직업대분류별 취업자 심층 분석 대시보드')
    
    df = load_data()
    
    # 주요 지표 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("전체 취업자 비율", "100%")
    with col2:
        st.metric("임금근로자 비율", "77.2%", "안정적")
    with col3:
        st.metric("상용직 비율", "74.1%", "높음")
    with col4:
        st.metric("고용 안정성 지수", 
                 f"{df['고용안정성_지수'].mean():.1f}",
                 "중상위")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs([
        '고용구조 분석', '고용안정성 분석', '상세세 분석'
    ])
    
    # 탭 1: 고용구조 분석
    with tab1:
        st.header('고용구조 종합 분석')
        
        # 전체 구조 분석
        fig_structure = create_job_distribution_chart(df)
        st.plotly_chart(fig_structure, use_container_width=True)
        
        # 직업별 분석
        st.subheader('직업별 상세 분석')
        selected_job = st.selectbox('분석할 직업 선택', df['직업대분류'].unique())
        
        col1, col2 = st.columns(2)
        with col1:
            # 선택된 직업의 고용형태 분포
            job_data = df[df['직업대분류'] == selected_job]
            emp_types = ['임금근로자', '상용', '임시일용', '비임금근로자']
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=job_data[emp_types].values[0],
                theta=emp_types,
                fill='toself',
                name=selected_job
            ))
            fig_radar.update_layout(title=f'{selected_job} 고용형태 분포')
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col2:
            # 선택된 직업의 주요 지표
            st.metric("임금근로자 비율", 
                     f"{job_data['임금근로자_비율'].values[0]:.1f}%")
            st.metric("상용직 비율",
                     f"{job_data['상용직_비율'].values[0]:.1f}%")
            st.metric("고용안정성 지수",
                     f"{job_data['고용안정성_지수'].values[0]:.1f}")
    
    # 탭 2: 고용안정성 분석
    with tab2:
        st.header('고용 안정성 종합 분석')
        
        # 안정성 차트
        fig_stability = create_stability_chart(df)
        st.plotly_chart(fig_stability, use_container_width=True)
        
        # 안정성 분석 결과
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            ### 높은 안정성 직군
            1. 관리자
            2. 전문가 및 관련 종사자
            3. 사무 종사자
            
            특징: 상용직 비율이 높고 임시일용직 비율이 낮음
            """)
        with col2:
            st.error("""
            ### 낮은 안정성 직군
            1. 단순노무 종사자
            2. 농림·어업 숙련 종사자
            3. 서비스 종사자
            
            특징: 임시일용직 또는 비임금근로자 비율이 높음
            """)
    
    # 탭 3: 상관관계 분석
    with tab3:
        st.header('고용형태 간 상관관계 분석')
        
        fig_corr = create_employment_analysis(df)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # 상관관계 해석
        st.info("""
        ### 📈 상관관계 주요 발견점
        1. 임금근로자와 상용직 간의 강한 양의 상관관계
        2. 상용직과 임시일용직 간의 음의 상관관계
        3. 비임금근로자와 다른 고용형태 간의 약한 상관관계
        
        이러한 패턴은 직업군별로 고용형태가 뚜렷하게 구분되어 있음을 시사합니다.
        """)

if __name__ == "__main__":
    main()
