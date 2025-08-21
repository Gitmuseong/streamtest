import streamlit as st
import random

# 후보 데이터
animals = [
    "강아지 🐶", "고양이 🐱", "토끼 🐰", "곰 🐻",
    "판다 🐼", "여우 🦊", "부엉이 🦉", "펭귄 🐧",
    "기린 🦒", "코알라 🐨", "사자 🦁", "다람쥐 🐿️",
    "북극곰 🐻‍❄️", "호랑이 🐯", "펠리컨 🐦", "원숭이 🐒"
]

# 세션 상태 초기화
if "round" not in st.session_state:
    st.session_state.round = 1
if "winners" not in st.session_state:
    st.session_state.winners = []
if "pairs" not in st.session_state:
    shuffled = animals.copy()
    random.shuffle(shuffled)
    st.session_state.pairs = [(shuffled[i], shuffled[i+1] if i+1 < len(shuffled) else None)
                              for i in range(0, len(shuffled), 2)]
if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("🐾 이승민 닮은 동물 이상형 월드컵 🐾")
st.write(f"**{st.session_state.round} 라운드**")

# 월드컵 진행
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
            if right:
                if st.button(right, key=f"right_{st.session_state.round}_{len(st.session_state.pairs)}"):
                    st.session_state.winners.append(right)
                    st.session_state.pairs.pop(0)
                    st.rerun()
            else:
                st.session_state.winners.append(left)
                st.session_state.pairs.pop(0)
                st.rerun()
    else:
        if len(st.session_state.winners) == 1:
            st.session_state.finished = True
            st.rerun()
        else:
            # 다음 라운드 생성: winners만 사용, 중복 방지
            next_round = st.session_state.winners.copy()
            st.session_state.winners = []
            random.shuffle(next_round)
            st.session_state.pairs = [(next_round[i], next_round[i+1] if i+1 < len(next_round) else None)
                                      for i in range(0, len(next_round), 2)]
            st.session_state.round += 1
            st.rerun()
else:
    st.success(f"🏆 최종 우승: **{st.session_state.winners[0]}**")
    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

