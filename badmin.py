import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="배드민턴 전체 대진 시스템", layout="wide")
LEVEL_WEIGHTS = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

st.title("🏸 라운드별 전체 대진 일정표")

# 2. 회원 데이터 관리 (최대 60명)
if 'members' not in st.session_state:
    st.session_state.members = []

# 3. 사이드바: 회원 등록
with st.sidebar:
    st.header("👥 회원 관리")
    with st.expander("➕ 신규 회원 등록"):
        if len(st.session_state.members) >= 60:
            st.warning("60명 정원 초과")
        else:
            n = st.text_input("이름")
            g = st.selectbox("성별", ["남", "여"])
            l = st.selectbox("급수", ["A", "B", "C", "D", "E"])
            if st.button("등록"):
                if n and not any(m['이름'] == n for m in st.session_state.members):
                    st.session_state.members.append({"이름": n, "성별": g, "급수": l})
                    st.rerun()
    
    if st.button("🧹 명단 초기화"):
        st.session_state.members = []
        st.rerun()

# 4. 참석자 선택
st.subheader("✅ 오늘 참석자 선택")
member_options = [f"{m['이름']}({m['성별']}/{m['급수']})" for m in st.session_state.members]
selected_list = st.multiselect("참석자를 체크하세요", options=member_options)

current_players = []
for opt in selected_list:
    name = opt.split("(")[0]
    p = next(m for m in st.session_state.members if m["이름"] == name)
    current_players.append(p)

st.info(f"현재 참여 인원: {len(current_players)}명")

# 5. 경기 설정
st.divider()
col_c, col_r = st.columns(2)
with col_c:
    num_courts = st.select_slider("🏟️ 가동 코트 수", options=[1, 2, 3, 4], value=min(len(current_players)//4, 4) if len(current_players)>=4 else 1)
with col_r:
    num_rounds = st.number_input("🔄 생성할 라운드 수 (경기 수)", min_value=1, max_value=10, value=3)

# 6. 전체 대진표 생성 및 나열
if st.button("📅 전체 라운드 일정 생성하기"):
    if len(current_players) < (num_courts * 4):
        st.error(f"인원이 부족합니다! {num_courts}개 코트를 돌리려면 최소 {num_courts * 4}명이 필요합니다.")
    else:
        st.success(f"총 {num_rounds}라운드의 대진표를 생성했습니다. 아래로 스크롤하며 확인하세요!")
        
        # 라운드별로 반복 생성
        for r in range(1, num_rounds + 1):
            st.markdown(f"## 🏆 제 {r} 라운드 (Match {r})")
            
            # 매 라운드마다 새로운 랜덤 조합을 위해 셔플
            random.seed(None)
            temp_players = current_players.copy()
            random.shuffle(temp_players)
            # 실력 균형을 위해 급수순 정렬
            sorted_players = sorted(temp_players, key=lambda x: LEVEL_WEIGHTS.get(x['급수'], 1), reverse=True)
            
            # 코트별 배치
            court_cols = st.columns(num_courts)
            for c in range(num_courts):
                with court_cols[c]:
                    pool = [sorted_players.pop(0) for _ in range(4)]
                    t1 = [pool[0], pool[3]]
                    t2 = [pool[1], pool[2]]
                    
                    st.markdown(f"**📍 {c+1}번 코트**")
                    st.code(f"TEAM A: {t1[0]['이름']}, {t1[1]['이름']}\n   VS   \nTEAM B: {t2[0]['이름']}, {t2[1]['이름']}")
            
            # 대기자 표시
            if sorted_players:
                rest = [p['이름'] for p in sorted_players]
                st.caption(f"💡 대기자: {', '.join(rest)}")
            
            st.divider() # 라운드 간 구분선

        st.balloons()
