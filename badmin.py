import streamlit as st
import random

st.set_page_config(page_title="선택 매칭기", layout="centered")

# 급수별 점수 (A: 5점 ~ E: 1점)
LEVEL_WEIGHTS = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

st.title("🏸 오늘 참석자 대진표")

# 1. 전체 회원 명단 관리 (세션 저장)
if 'members' not in st.session_state:
    # 기본 데이터 (테스트용)
    st.session_state.members = [
        {"이름": "강백호", "성별": "남", "급수": "A"},
        {"이름": "서태웅", "성별": "남", "급수": "A"},
        {"이름": "채치수", "성별": "남", "급수": "B"},
        {"이름": "송태섭", "성별": "남", "급수": "C"},
        {"이름": "정대만", "성별": "남", "급수": "B"},
        {"이름": "안경선배", "성별": "남", "급수": "D"},
        {"이름": "소연", "성별": "여", "급수": "E"},
        {"이름": "한나", "성별": "여", "급수": "C"}
    ]

# 2. 새로운 회원 추가 (사이드바)
with st.sidebar.expander("➕ 신규 회원 등록"):
    new_n = st.text_input("이름")
    new_g = st.selectbox("성별", ["남", "여"])
    new_l = st.selectbox("급수", ["A", "B", "C", "D", "E"])
    if st.button("회원 추가"):
        if new_n:
            st.session_state.members.append({"이름": new_n, "성별": new_g, "급수": new_l})
            st.rerun()

# 3. 중요!! 오늘 참석자 선택 (멀티셀렉트)
st.subheader("✅ 오늘 운동 나온 사람 선택")
member_names = [m["이름"] for m in st.session_state.members]
selected_names = st.multiselect(
    "이름을 검색하거나 선택하세요 (최소 4명)",
    options=member_names,
    default=[] # 처음엔 아무도 선택 안 된 상태
)

# 선택된 사람들의 상세 데이터만 추출
present_players = [m for m in st.session_state.members if m["이름"] in selected_names]

st.info(f"현재 선택된 인원: {len(present_players)}명")

# 4. 매칭 버튼 및 로직
if st.button("🎯 대진표 생성하기"):
    if len(present_players) < 4:
        st.error("최소 4명 이상 선택해야 경기를 잡을 수 있습니다!")
    else:
        # 급수 점수 부여 및 셔플
        for p in present_players:
            p['score'] = LEVEL_WEIGHTS.get(p['급수'], 1)
        
        random.shuffle(present_players)
        # 실력순 정렬
        sorted_players = sorted(present_players, key=lambda x: x['score'], reverse=True)
        
        st.divider()
        st.subheader("🏟️ 코트 배정 결과")
        
        court_num = 1
        # 4명씩 끊어서 매칭 (최대 4개 코트)
        while len(sorted_players) >= 4 and court_num <= 4:
            # 실력 균형을 위해 [1등, 4등] vs [2등, 3등] 조합
            pool = [sorted_players.pop(0) for _ in range(4)]
            pool.sort(key=lambda x: x['score'], reverse=True)
            
            team1 = [pool[0], pool[3]] # 최상 + 최하
            team2 = [pool[1], pool[2]] # 중간 + 중간
            
            st.markdown(f"#### {court_num}번 코트")
            c1, vs, c2 = st.columns([4, 1, 4])
            with c1:
                st.success(f"**팀 A**\n\n{team1[0]['이름']}({team1[0]['급수']}) / {team1[1]['이름']}({team1[1]['급수']})")
            with vs:
                st.write("\n\nVS")
            with c2:
                st.info(f"**팀 B**\n\n{team2[0]['이름']}({team2[0]['급수']}) / {team2[1]['이름']}({team2[1]['급수']})")
            
            court_num += 1
            st.write("")

        # 남은 인원 알림
        if len(sorted_players) > 0:
            rest_names = [p['이름'] for p in sorted_players]
            st.warning(f"💡 대기 인원: {', '.join(rest_names)}")

# 명단 삭제 기능
if st.sidebar.button("🧹 전체 명단 초기화"):
    st.session_state.members = []
    st.rerun()