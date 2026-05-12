import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 데이터베이스 연결 설정
conn = sqlite3.connect('data.db') # 실제 데이터베이스 파일명으로 변경 필요

def run_query(query):
    return pd.read_sql_query(query, conn)

st.set_page_config(layout="wide")
st.title("🚇 대중교통 분실물 데이터 분석 대시보드")

# ==========================================
# 1. 우천 시 분실물이 늘어날까?
# ==========================================
st.header("1. 우천 시 분실물이 늘어날까?")

sql1 = """
SELECT 강수량.날짜, SUM(강수량.강수량) AS 일별강수량, COUNT(습득물.접수번호) AS 분실물수
FROM 강수량
LEFT JOIN 습득물 ON 강수량.날짜 = 습득물.날짜
GROUP BY 강수량.날짜
ORDER BY 강수량.날짜;
"""
df1 = run_query(sql1)

# 이중축 차트 생성
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Bar(x=df1['날짜'], y=df1['일별강수량'], name="일별 강수량"), secondary_y=False)
fig1.add_trace(go.Scatter(x=df1['날짜'], y=df1['분실물수'], name="분실물 수", mode='lines+markers'), secondary_y=True)

st.plotly_chart(fig1, use_container_width=True)
st.subheader("(2) 사용한 SQL 코드")
st.code(sql1, language='sql')
st.subheader("(3) 인사이트")
st.info("- 일부 일자를 제외하고, 주로 일별 강수량이 높을 때마다 분실물 수가 늘어나는 경향을 보인다. 이는 우산, 우비와 같이 챙겨야 하는 물품이 많을수록 분실물이 발생하기 쉬움임을 확인할 수 있는 지표이다. 우천 시에는 분실물 주의 안내방송 횟수를 늘리고, 전광판에 분실물 주의 화면을 자주 재생하도록 한다.")

st.divider()

# ==========================================
# 2. 교통량이 많은 지역일수록 분실물이 많을까?
# ==========================================
st.header("2. 교통량이 많은 지역일수록 분실물이 많을까?")

# 쿼리 1: 분실물이 많은 지역(회사) 순위
sql2_1 = """
SELECT 습득물.회사, 회사정보.자치구명, COUNT(*) AS 분실물수
FROM 습득물
LEFT JOIN 회사정보 ON 습득물.회사 = 회사정보.회사
GROUP BY 습득물.회사, 회사정보.자치구명
ORDER BY 분실물수 DESC
LIMIT 5;
"""

# 쿼리 2: 자치구별 총 교통량
sql2_2 = """
SELECT 자치구명, SUM(통행건수) AS 총교통량
FROM 교통량
GROUP BY 자치구명
ORDER BY 총교통량 DESC;
"""

df2_1 = run_query(sql2_1)
df2_2 = run_query(sql2_2)

# 화면 레이아웃 (좌: 차트, 우: 교통량 테이블)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("분실물 상위 5개 지역")
    fig2 = go.Figure(go.Bar(
        x=df2_1['분실물수'], 
        y=df2_1['회사'] + " (" + df2_1['자치구명'] + ")", 
        orientation='h'
    ))
    fig2.update_layout(yaxis=dict(autorange="reversed")) # 순위 높은 순으로 위로
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("자치구별 교통량 순위")
    st.dataframe(df2_2, use_container_width=True)

st.subheader("(2) 사용한 SQL 코드")
with st.expander("SQL 코드 보기"):
    st.code(sql2_1, language='sql')
    st.code(sql2_2, language='sql')

st.subheader("(3) 인사이트")
st.info("""
- 교통량과 환승 구간에 해당하는 지역일수록 이동 과정에서 분실물이 발생하기 쉬울 것이라 예상했다. 
- 구내 교통량은 강남구, 관악구, 송파구, 강서구, 은평구 순이다. 
- 총 교통량 5위인 은평구가 습득물 수 4위에 있으나, 이 정보만으로는 두 요소 간 상관관계를 유의미하게 확인하기 어렵다. 
- 외부 지역으로부터 오는 버스의 데이터로 보완할 필요가 있다.
""")

# ==========================================
# 3. 버스 회사의 운행 횟수와 분실물 습득 횟수는 비례할까?
# ==========================================
st.header("3. 버스 회사의 운행 횟수와 분실물 습득 횟수는 비례할까?")

sql3 = """
SELECT 습득물.회사, COUNT(*) AS 분실물수, SUM(운행정보.총운행횟수) AS 총운행횟수
FROM 습득물
LEFT JOIN 운행정보 ON 습득물.회사 = 운행정보.회사
GROUP BY 습득물.회사
ORDER BY 분실물수 DESC;
"""

df3 = run_query(sql3)

# 산점도 생성
fig3 = go.Figure(data=go.Scatter(
    x=df3['총운행횟수'], 
    y=df3['분실물수'], 
    mode='markers+text',
    text=df3['회사'],
    textposition="top center",
    marker=dict(size=12, color='coral')
))

fig3.update_layout(
    xaxis_title="총 운행 횟수",
    yaxis_title="분실물 습득 수"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("(2) 사용한 SQL 코드")
with st.expander("SQL 코드 보기"):
    st.code(sql3, language='sql')

st.subheader("(3) 인사이트")
st.info("""
- 분실물 수 순위와 총 운행횟수 순위가 같다. 운행 횟수가 많은 노선일수록 분실물이 많이 발생한다. 
- 다만, 분실 신고가 접수되거나 본인 요청이 있는 경우만 기록되고 있으므로, 실제 분실물은 더 많을 것으로 추산된다. 
- 이 5개 회사에 대해서는 분실물 신고에 대한 캠페인을 진행하는 것도 긍정적인 효과를 불러올 수 있다고 판단된다.
""")