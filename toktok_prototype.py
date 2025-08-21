import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import uuid
import plotly.express as px

# ------------------------
# 페이지 설정
# ------------------------
st.set_page_config(
    page_title="톡톡 상담 지원 시스템",
    page_icon="💬",
    layout="wide"
)

# ------------------------
# CSS 스타일링
# ------------------------
# 채팅 메시지 및 전체 UI 스타일을 정의합니다.
st.markdown("""
<style>
.chat-message {
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 12px;
    max-width: 70%;
    word-wrap: break-word;
}
.user-message {
    background: #E3F2FD;
    margin-left: 30%;
    border: 1px solid #bbdefb;
}
.counselor-message {
    background: #F1F8E9;
    margin-right: 30%;
    border: 1px solid #dcedc8;
}
/* 대시보드 메트릭 박스 스타일 */
.stMetric {
    background-color: #F8F9FA;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #E0E0E0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
/* 전체 페이지 배경색 */
.main {
    background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# 샘플 데이터 생성
# ------------------------
# @st.cache_data를 사용하여 데이터를 한 번만 생성하고 캐시합니다.
@st.cache_data
def generate_sample_data():
    customer_names = ["김민준", "이서연", "박도윤", "정시우", "최예은", "김하준", "이서진", "박건우"]
    counselor_names = ["상담사-A", "상담사-B", "상담사-C", "상담사-D"]
    topics = ["대출 조건 문의", "적금 상품 안내", "주택담보대출 상담", "인터넷뱅킹 오류", "카드 분실 신고"]
    data = []
    for i in range(200):  # 샘플 건수 증가
        consultation_date = datetime.now() - timedelta(days=random.randint(0, 90))
        data.append({
            "상담자": random.choice(customer_names),
            "상담사": random.choice(counselor_names), # 새로운 '상담사' 필드 추가
            "상담 내용 요약": random.choice(topics),
            "상담일": consultation_date.strftime("%Y-%m-%d"),
            "상담 시간": f"{random.randint(9, 17):02d}:{random.randint(0, 59):02d}",
            "상담 소요 시간(분)": random.randint(3, 30), # 새로운 '상담 소요 시간' 필드 추가
            "만족도 점수": random.choice([1, 2, 3, 4, 5]), # 새로운 '만족도 점수' 필드 추가
            "상담 ID": str(uuid.uuid4())[:8]
        })
    return pd.DataFrame(data)

# ------------------------
# 상담 상세 대화 생성
# ------------------------
def generate_consultation_detail(summary):
    return [
        {"speaker": "고객", "message": f"안녕하세요, {summary}에 대해 문의드립니다."},
        {"speaker": "상담사", "message": "안녕하세요, 상담사입니다. 자세히 안내드리겠습니다."},
    ]

# ------------------------
# 세션 초기화
# ------------------------
# 필요한 세션 상태 변수들을 초기화합니다.
if "sample_data" not in st.session_state:
    st.session_state.sample_data = generate_sample_data()
if "selected_consultation" not in st.session_state:
    st.session_state.selected_consultation = None
if "page" not in st.session_state:
    st.session_state.page = "메인"

# ------------------------
# 페이지별 함수
# ------------------------
def main_page():
    st.markdown("### 상담 이력")
    
    search_name = st.text_input("상담자 이름 검색")
    df = st.session_state.sample_data.copy()
    
    # 상담자 이름으로 필터링
    if search_name:
        df_filtered = df[df["상담자"].str.contains(search_name)]
    else:
        df_filtered = df
    
    if df_filtered.empty:
        st.info("조회된 상담 내역이 없습니다.")
        return
    
    # 새로운 표 형태 (헤더 + 데이터 행 + 버튼)로 출력
    
    # 1. 표의 헤더를 만듭니다.
    header_cols = st.columns([2, 2, 3, 2, 2, 1])
    header_cols[0].markdown("**상담자**")
    header_cols[1].markdown("**상담사**")
    header_cols[2].markdown("**상담 내용 요약**")
    header_cols[3].markdown("**상담일**")
    header_cols[4].markdown("**상담 시간**")
    header_cols[5].markdown("**상세**")
    st.markdown("---")
    
    # 2. 데이터를 반복하며 각 행과 버튼을 생성합니다.
    for i, row in df_filtered.iterrows():
        # 데이터 행을 담을 열을 만듭니다.
        row_cols = st.columns([2, 2, 3, 2, 2, 1])
        
        # 각 열에 데이터 출력
        row_cols[0].write(row["상담자"])
        row_cols[1].write(row["상담사"])
        row_cols[2].write(row["상담 내용 요약"])
        row_cols[3].write(row["상담일"])
        row_cols[4].write(row["상담 시간"])
        
        # 마지막 열에 '상세보기' 버튼 추가
        # key는 버튼마다 고유해야 하므로 상담 ID를 사용합니다.
        if row_cols[5].button("상세보기", key=row["상담 ID"]):
            st.session_state.selected_consultation = row
            st.session_state.page = "상담 상세"
            st.rerun() # 페이지 전환을 위해 rerunning
            
def new_consultation_page():
    st.markdown("### ➕ 새 상담 시작")
    st.info("새 상담 진행 UI (프로토타입)")

def consultation_detail_page():
    if st.session_state.selected_consultation is None:
        st.warning("상담을 선택하세요.")
        return
    consult = st.session_state.selected_consultation
    st.markdown("### 상담 상세")
    st.markdown(f"**상담자:** {consult['상담자']}  |  **상담사:** {consult['상담사']}  |  **날짜:** {consult['상담일']} {consult['상담 시간']}")
    st.markdown(f"**요약:** {consult['상담 내용 요약']}  |  **소요 시간:** {consult['상담 소요 시간(분)']}분  |  **만족도:** {consult['만족도 점수']}점")
    st.markdown("---")
    for conv in generate_consultation_detail(consult["상담 내용 요약"]):
        if conv["speaker"] == "고객":
            st.markdown(f'<div class="chat-message user-message"><strong>{consult["상담자"]}</strong><br>{conv["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message counselor-message"><strong>{consult["상담사"]}</strong><br>{conv["message"]}</div>', unsafe_allow_html=True)

    # 메인으로 돌아가기 버튼
    if st.button("⬅ 메인으로 돌아가기"):
        st.session_state.page = "메인"
        st.session_state.selected_consultation = None
        st.rerun()

def dashboard_page():
    """상담 데이터를 시각화하는 대시보드 페이지 함수입니다."""
    st.markdown("### 상담사 대시보드")
    df = st.session_state.sample_data.copy()
    df['상담_datetime'] = pd.to_datetime(df['상담일'] + ' ' + df['상담 시간'])
    
    # --- 주요 지표 (KPI) ---
    st.markdown("#### 주요 지표")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_consultations = len(df)
        st.metric("총 상담 건수", total_consultations)
    with col2:
        today_count = df[df['상담_datetime'].dt.date == datetime.now().date()].shape[0]
        st.metric("오늘 누적 상담 건수", today_count)
    with col3:
        avg_duration = df['상담 소요 시간(분)'].mean().round(1)
        st.metric("평균 상담 소요 시간", f"{avg_duration}분")
    with col4:
        avg_satisfaction = df['만족도 점수'].mean().round(2)
        st.metric("평균 만족도 점수", f"{avg_satisfaction}점")
    st.markdown("---")

    # --- 상담사별 성과 분석 ---
    st.markdown("#### 상담사별 성과 분석")
    col5, col6 = st.columns(2)
    
    with col5:
        # 상담사별 상담 건수 막대 그래프
        counselor_counts = df.groupby('상담사').size().reset_index(name='건수').sort_values('건수', ascending=False)
        fig_counselor_counts = px.bar(counselor_counts, x='상담사', y='건수', title="상담사별 상담 건수",
                                      labels={'상담사': '상담사', '건수': '상담 건수'}, color='상담사')
        st.plotly_chart(fig_counselor_counts, use_container_width=True)

    with col6:
        # 상담사별 평균 상담 소요 시간 막대 그래프
        counselor_avg_duration = df.groupby('상담사')['상담 소요 시간(분)'].mean().reset_index(name='평균 소요 시간(분)').sort_values('평균 소요 시간(분)', ascending=False)
        fig_counselor_duration = px.bar(counselor_avg_duration, x='상담사', y='평균 소요 시간(분)', title="상담사별 평균 소요 시간",
                                        labels={'상담사': '상담사', '평균 소요 시간(분)': '평균 소요 시간(분)'}, color='상담사')
        st.plotly_chart(fig_counselor_duration, use_container_width=True)
    st.markdown("---")

    # --- 고객 만족도 및 상담 추이 분석 ---
    st.markdown("#### 고객 만족도 및 상담 추이")
    
    # 만족도 점수 분포 파이 차트
    satisfaction_counts = df['만족도 점수'].value_counts().reset_index()
    satisfaction_counts.columns = ['만족도 점수', '건수']
    fig_satisfaction = px.pie(satisfaction_counts, names='만족도 점수', values='건수', title="만족도 점수 분포")
    st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    # 시간대별 상담 건수 막대 그래프 (기존)
    hourly_counts = df.groupby(df['상담_datetime'].dt.hour).size().reset_index(name='건수')
    hourly_counts.columns = ['시간대', '건수']
    fig_hourly = px.bar(hourly_counts, x='시간대', y='건수', title="시간대별 상담 건수",
                        labels={'시간대': '시간', '건수': '상담 건수'})
    st.plotly_chart(fig_hourly, use_container_width=True)

    # 상담 주제별 비율 파이 차트 (기존)
    topic_counts = df['상담 내용 요약'].value_counts().reset_index()
    topic_counts.columns = ['상담 주제', '건수']
    fig_topic = px.pie(topic_counts, names='상담 주제', values='건수', title="상담 주제별 비율")
    st.plotly_chart(fig_topic, use_container_width=True)
    
    # 최근 7일 상담 추이 라인 차트 (기존)
    df_last7 = df[df['상담_datetime'].dt.date >= (datetime.now().date() - pd.Timedelta(days=6))]
    daily_counts = df_last7.groupby(df_last7['상담_datetime'].dt.date).size().reset_index(name='건수')
    fig_daily = px.line(daily_counts, x='상담_datetime', y='건수', markers=True, title="최근 7일 상담 추이")
    st.plotly_chart(fig_daily, use_container_width=True)
    
# ------------------------
# 사이드바 메뉴
# ------------------------
with st.sidebar:
    st.markdown("## 메뉴")
    menu_options = ["메인", "새 상담", "상담 상세", "상담 대시보드"]
    menu = st.radio(
        "이동", 
        menu_options, 
        index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
    )
    st.session_state.page = menu

# ------------------------
# 페이지 표시
# ------------------------
# 세션 상태 변수 `page`에 따라 다른 함수를 호출하여 페이지를 렌더링합니다.
if st.session_state.page == "메인":
    main_page()
elif st.session_state.page == "새 상담":
    new_consultation_page()
elif st.session_state.page == "상담 상세":
    consultation_detail_page()
elif st.session_state.page == "상담 대시보드":
    dashboard_page()
