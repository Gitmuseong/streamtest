import streamlit as st
import random

st.title("🐯 상원고 3학년 9반 이승민 닮은 동물 이상형 월드컵 🐼")

# 동물 후보 리스트
animals = [
    "🐶 강아지", "🐱 고양이", "🦊 여우", "🐯 호랑이",
    "🐼 판다", "🐧 펭귄", "🐸 개구리", "🦁 사자",
    "🐰 토끼", "🐻 곰", "🐨 코알라", "🦉 부엉이"
]

if "pairs" not in st.session_state:
    random.shuffle(animals)
    st.session_state.pairs = [(animals[i], animals[i+1]) for i in range(0, len(animals), 2)]
    st.session_state.round = 1
    st.session_state.winners = []
    st.session_state.finished = False

st.subheader(f"Round {st.session_state.round}")

if st.session_state.finished:
    st.success(f"🏆 최종 승자는 {st.session_state.winners[0]} 입니다! 🎉")
else:
    for i, (a, b) in enumerate(st.session_state.pairs):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(a, key=f"a_{i}"):
                st.session_state.winners.append(a)
                if len(st.session_state.winners) == len(st.session_state.pairs):
                    st.session_state.pairs = [(st.session_state.winners[i], st.session_state.winners[i+1]) 
                                              for i in range(0, len(st.session_state.winners), 2)]
                    st.session_state.round += 1
                    st.session_state.winners = []
                    if len(st.session_state.pairs) == 1:
                        st.session_state.finished = True
                st.rerun()
        with col2:
            if st.button(b, key=f"b_{i}"):
                st.session_state.winners.append(b)
                if len(st.session_state.winners) == len(st.session_state.pairs):
                    st.session_state.pairs = [(st.session_state.winners[i], st.session_state.winners[i+1]) 
                                              for i in range(0, len(st.session_state.winners), 2)]
                    st.session_state.round += 1
                    st.session_state.winners = []
                    if len(st.session_state.pairs) == 1:
                        st.session_state.finished = True
                st.rerun()
