import streamlit as st
import random
# --- 후보 데이터 ---
animals = [
    "강아지 🐶",
    "고양이 🐱",
    "토끼 🐰",
    "곰 🐻",
    "판다 🐼",
    "여우 🦊",
    "부엉이 🦉",
    "펭귄 🐧"
    "기린 🦒"
]

# --- 세션 상태 초기화 ---
if "round" not in st.session_state:
    st.session_state.round = 1
if "pairs" not in st.session_state:
    shuffled = animals.copy()
    random.shuffle(shuffled)
    st.session_state.pairs = [(shuffled[i], shuffled[i+1]) for i in range(0, len(shuffled), 2)]
if "winners" not in st.session_state:
    st.session_state.winners = []
if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("🐾 이승민 닮은 동물 이상형 월드컵 🐾")
st.write(f"**{st.session_state.round} 라운드**")

# --- 월드컵 진행 ---
if not st.session_state.finished:
    if st.session_state.pairs:
        left, right = st.session_state.pairs[0]
        col1, col2 = st.columns(2)

        with col1:
            if st.button(left, key=f"left_{st.session_state.round}_{len(st.session_state.pairs)}"):
                st.session_state.winners.append(left)
                st.session_state.pairs.pop(0)
                st.rerun()

        with col2:
            if st.button(right, key=f"right_{st.session_state.round}_{len(st.session_state.pairs)}"):
                st.session_state.winners.append(right)
                st.session_state.pairs.pop(0)
                st.rerun()
    else:
        # 라운드 종료 후 다음 라운드 준비
        if len(st.session_state.winners) == 1:
            st.session_state.finished = True
            st.rerun()
        else:
            random.shuffle(st.session_state.winners)
            st.session_state.pairs = [
                (st.session_state.winners[i], st.session_state.winners[i+1])
                for i in range(0, len(st.session_state.winners), 2)]
            st.session_state.winners = []
            st.session_state.round += 1
            st.rerun()
else:
    st.success(f"🏆 최종 우승: **{st.session_state.winners[0]}**")
    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
