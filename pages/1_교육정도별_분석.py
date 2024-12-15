import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_data():
    # 중졸 이하 데이터
    junior_data = {
        '교육정도': ['중졸이하'] * 5,
        '직업분류': ['청소 및 경비 관련 단순 노무직', '농·축산 숙련직', 
                  '조리 및 음식 서비스직', '돌봄·보건 및 개인 생활 서비스직',
                  '운전 및 운송 관련직'],
        '2023상반기': [785, 817, 238, 214, 208],
        '2024상반기': [790, 783, 225, 213, 200],
        '취업자증감': [5, -35, -14, -1, -7],
        '구성비증감': [1.1, 0.0, -0.1, 0.2, 0.0]
    }

    # 고졸 데이터
    high_data = {
        '교육정도': ['고졸'] * 5,
        '직업분류': ['경영 및 회계 관련 사무직', '조리 및 음식 서비스직',
                  '매장 판매 및 상품 대여직', '운전 및 운송 관련직',
                  '돌봄·보건 및 개인 생활 서비스직'],
        '2023상반기': [1025, 948, 889, 767, 553],
        '2024상반기': [995, 969, 841, 790, 570],
        '취업자증감': [-29, 21, -48, 23, 16],
        '구성비증감': [-0.1, 0.3, -0.4, 0.3, 0.2]
    }

    # 대졸 이상 데이터
    college_data = {
        '교육정도': ['대졸이상'] * 5,
        '직업분류': ['경영 및 회계 관련 사무직', '보건·사회복지 및 종교 관련직',
                  '교육 전문가 및 관련직', '공학 전문가 및 기술직',
                  '문화·예술·스포츠 전문가 및 관련직'],
        '2023상반기': [3099, 1429, 1157, 954, 649],
        '2024상반기': [3233, 1440, 1137, 1018, 705],
        '취업자증감': [134, 11, -21, 63, 56],
        '구성비증감': [0.2, -0.3, -0.4, 0.2, 0.2]
    }

    df = pd.concat([
        pd.DataFrame(junior_data),
        pd.DataFrame(high_data),
        pd.DataFrame(college_data)
    ])
    
    # 총계 계산
    df['2023총계'] = df.groupby('교육정도')['2023상반기'].transform('sum')
    df['2024총계'] = df.groupby('교육정도')['2024상반기'].transform('sum')
    df['비중_2023'] = (df['2023상반기'] / df['2023총계'] * 100).round(1)
    df['비중_2024'] = (df['2024상반기'] / df['2024총계'] * 100).round(1)
    
    return df

def create_total_comparison(df):
    totals = df.groupby('교육정도').agg({
        '2023총계': 'first',
        '2024총계': 'first'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='2023년',
        x=totals['교육정도'],
        y=totals['2023총계'],
        marker_color='royalblue'
    ))
    
    fig.add_trace(go.Bar(
        name='2024년',
        x=totals['교육정도'],
        y=totals['2024총계'],
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title='교육정도별 취업자 수 비교',
        barmode='group',
        xaxis_title='교육정도',
        yaxis_title='취업자 수 (명)'
    )
    
    return fig

def create_composition_chart(df, year):
    year_col = f'{year}상반기'
    df_year = df.copy()
    df_year['비율'] = (df_year[year_col] / df_year.groupby('교육정도')[year_col].transform('sum') * 100).round(1)
    
    fig = px.sunburst(
        df_year,
        path=['교육정도', '직업분류'],
        values=year_col,
        title=f'{year}년 교육정도별 직업분포',
        color='비율',
        color_continuous_scale='Blues'
    )
    
    return fig

def create_change_heatmap(df):
    pivot_data = df.pivot(index='교육정도', columns='직업분류', values='구성비증감')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        text=np.round(pivot_data.values, 1),
        texttemplate='%{text}',
        colorscale='RdBu',
        colorbar_title='구성비 변화(%p)'
    ))
    
    fig.update_layout(
        title='교육정도별 직업 구성비 변화(2023→2024)',
        xaxis_title='직업분류',
        yaxis_title='교육정도',
        height=400
    )
    
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title('교육정도별 직업분류별 취업자 분석 대시보드')
    
    df = load_data()

    # 교육정도별 취업자 현황
    st.header('교육정도별 취업자 전체 현황')
    
    # 데이터 준비
    total_change = df['취업자증감'].sum()
    max_increase_idx = df['취업자증감'].idxmax()
    max_decrease_idx = df['취업자증감'].idxmin()
    
    # 값 추출
    max_increase_val = df['취업자증감'].values[max_increase_idx]
    max_decrease_val = df['취업자증감'].values[max_decrease_idx]
    max_increase_edu = df['교육정도'].values[max_increase_idx]
    max_increase_job = df['직업분류'].values[max_increase_idx]
    max_decrease_edu = df['교육정도'].values[max_decrease_idx]
    max_decrease_job = df['직업분류'].values[max_decrease_idx]

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "전체 취업자 변동",
            f"{total_change:,}명",
            delta=int(total_change)  # total_change를 int로 변환
        )
    with col2:
        st.metric(
            "가장 큰 증가",
            f"{max_increase_edu} - {max_increase_job}",
            delta=int(max_increase_val)  # max_increase_val를 int로 변환
        )
    with col3:
        st.metric(
            "가장 큰 감소",
            f"{max_decrease_edu} - {max_decrease_job}",
            delta=int(max_decrease_val)  # max_decrease_val를 int로 변환
        )

    # 나머지 코드는 동일하게 유지
    fig_total = create_total_comparison(df)
    st.plotly_chart(fig_total, use_container_width=True)
    
    st.header('교육정도별 직업 분포 분석')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('2023년 직업 분포')
        fig_2023 = create_composition_chart(df, '2023')
        st.plotly_chart(fig_2023, use_container_width=True)
        
    with col2:
        st.subheader('2024년 직업 분포')
        fig_2024 = create_composition_chart(df, '2024')
        st.plotly_chart(fig_2024, use_container_width=True)
    
    st.header('구성비 변화 분석')
    fig_heatmap = create_change_heatmap(df)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.header('교육정도별 상세 분석')
    selected_edu = st.selectbox('교육정도 선택', df['교육정도'].unique())
    
    edu_data = df[df['교육정도'] == selected_edu]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_edu = go.Figure()
        fig_edu.add_trace(go.Bar(
            name='2023년',
            x=edu_data['직업분류'],
            y=edu_data['비중_2023'],
            marker_color='royalblue'
        ))
        fig_edu.add_trace(go.Bar(
            name='2024년',
            x=edu_data['직업분류'],
            y=edu_data['비중_2024'],
            marker_color='lightblue'
        ))
        fig_edu.update_layout(
            title=f'{selected_edu} 직업별 비중 변화',
            barmode='group',
            xaxis_tickangle=45
        )
        st.plotly_chart(fig_edu, use_container_width=True)
    
    with col2:
        st.subheader('주요 변화')
        max_increase = edu_data.iloc[edu_data['취업자증감'].idxmax()]
        max_decrease = edu_data.iloc[edu_data['취업자증감'].idxmin()]
        
        st.info(f"""
        **가장 큰 증가**
        - 직업: {max_increase['직업분류']}
        - 증가량: {max_increase['취업자증감']}명
        - 구성비 변화: {max_increase['구성비증감']}%p
        """)
        
        st.warning(f"""
        **가장 큰 감소**
        - 직업: {max_decrease['직업분류']}
        - 감소량: {max_decrease['취업자증감']}명
        - 구성비 변화: {max_decrease['구성비증감']}%p
        """)

if __name__ == "__main__":
    main()
