import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_data():
    # 2024년 상반기 데이터
    data_2024 = {
        '직업대분류': ['관리자', '전문가 및 관련 종사자', '사무 종사자', '서비스 종사자', 
                    '판매 종사자', '농림·어업 숙련 종사자', '기능원 및 관련 기능 종사자',
                    '장치·기계 조작 및 조립 종사자', '단순노무 종사자'],
        '임금근로자': [413, 5359, 4780, 2495, 1457, 58, 1695, 2188, 3695],
        '100만원미만': [0.0, 2.1, 1.8, 22.0, 11.9, 1.4, 1.0, 0.9, 30.1],
        '100-200만원': [0.2, 6.1, 4.3, 22.2, 15.9, 13.7, 5.7, 4.4, 22.9],
        '200-300만원': [3.5, 27.4, 33.3, 35.7, 37.7, 47.1, 28.8, 33.9, 36.4],
        '300-400만원': [8.4, 23.4, 26.2, 12.4, 20.5, 26.9, 35.5, 33.5, 9.4],
        '400만원이상': [88.0, 40.9, 34.4, 7.7, 14.0, 11.1, 29.0, 27.3, 1.1]
    }
    
    return pd.DataFrame(data_2024)

def main():
    st.set_page_config(layout="wide")
    st.title('직업대분류별 임금 분포 현황 대시보드')
    st.markdown("### 2024년 상반기 임금근로자 급여 분석")
    
    df = load_data()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(['임금 수준 개요', '직종별 급여 분포', '상세 분석'])
    
    # 탭 1: 임금 수준 개요
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # 직종별 임금근로자 수
            fig_workers = px.bar(df,
                               x='직업대분류',
                               y='임금근로자',
                               title='직종별 임금근로자 수',
                               text='임금근로자')
            fig_workers.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_workers, use_container_width=True)
        
        with col2:
            # 400만원 이상 비율
            fig_high_salary = px.bar(df,
                                   x='직업대분류',
                                   y='400만원이상',
                                   title='직종별 고임금(400만원 이상) 비율',
                                   text=df['400만원이상'].apply(lambda x: f'{x:.1f}%'))
            fig_high_salary.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_high_salary, use_container_width=True)
        
        # 임금 구간별 히트맵
        salary_columns = ['100만원미만', '100-200만원', '200-300만원', '300-400만원', '400만원이상']
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df[salary_columns].values,
            x=salary_columns,
            y=df['직업대분류'],
            text=df[salary_columns].values.round(1),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorscale='Blues',
            colorbar_title='비율 (%)'
        ))
        fig_heatmap.update_layout(
            title='직종별 임금 분포 현황 (단위: %)',
            height=600
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # 탭 2: 직종별 급여 분포
    with tab2:
        # 직종 선택 드롭다운
        selected_job = st.selectbox(
            '직종을 선택하세요',
            df['직업대분류'].tolist()
        )
        
        # 선택된 직종의 급여 분포
        selected_data = df[df['직업대분류'] == selected_job].iloc[0]
        salary_dist = pd.DataFrame({
            '임금구간': salary_columns,
            '비율': [selected_data[col] for col in salary_columns]
        })
        
        fig_dist = px.bar(salary_dist,
                         x='임금구간',
                         y='비율',
                         title=f'{selected_job} 임금 분포',
                         text='비율')
        fig_dist.update_traces(texttemplate='%{text:.1f}%')
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # 통계 정보
        st.markdown(f"""
        #### {selected_job} 주요 통계
        - 임금근로자 수: {selected_data['임금근로자']:,}명
        - 중위임금 구간: 200-300만원
        - 고임금(400만원 이상) 비율: {selected_data['400만원이상']:.1f}%
        - 저임금(200만원 미만) 비율: {selected_data['100만원미만'] + selected_data['100-200만원']:.1f}%
        """)

    # 탭 3: 상세 분석
    with tab3:
        st.header('임금 수준별 분석')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 저임금 비율
            df['저임금비율'] = df['100만원미만'] + df['100-200만원']
            fig_low = px.pie(df,
                           values='저임금비율',
                           names='직업대분류',
                           title='직종별 저임금(200만원 미만) 근로자 비율')
            st.plotly_chart(fig_low, use_container_width=True)
            
        with col2:
            # 중위임금 비율
            fig_mid = px.pie(df,
                           values='200-300만원',
                           names='직업대분류',
                           title='직종별 중위임금(200-300만원) 근로자 비율')
            st.plotly_chart(fig_mid, use_container_width=True)
        
        # 전체 임금 분포 요약
        st.markdown("""
        ### 주요 발견사항
        1. **고임금 직종**
           - 관리자의 88%가 400만원 이상의 급여를 받고 있음
           - 전문가 및 관련 종사자의 40.9%가 400만원 이상의 급여 구간에 속함
        
        2. **저임금 직종**
           - 단순노무 종사자의 53%가 200만원 미만의 급여를 받고 있음
           - 서비스 종사자의 44.2%가 200만원 미만의 급여 구간에 속함
        
        3. **중위임금 집중 직종**
           - 농림·어업 숙련 종사자의 47.1%가 200-300만원 구간에 집중
           - 판매 종사자의 37.7%가 200-300만원 구간에 분포
        """)

if __name__ == '__main__':
    main()
