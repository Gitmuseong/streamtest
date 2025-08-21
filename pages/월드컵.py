import streamlit as st
import random

st.title("🐾 씅민이 동물상 이상형 월드컵 🐾")

# 세션 상태 초기화
if "candidates" not in st.session_state:
    st.session_state.candidates = [
        "강아지상", "고양이상", "여우상", "판다상",
        "토끼상", "곰상", "부엉이상", "호랑이상"
    ]
if "round" not in st.session_state:
    st.session_state.round = 1
if "pairs" not in st.session_state:
    random.shuffle(st.session_state.candidates)
    st.session_state.pairs = [
        st.session_state.candidates[i:i+2]
        for i in range(0, len(st.session_state.candidates), 2)
    ]
if "winners" not in st.session_state:
    st.session_state.winners = []

st.write(f"### Round {st.session_state.round}")

# 현재 대진 표시
if st.session_state.pairs:
    pair = st.session_state.pairs[0]
    st.write("다음 두 동물상 중 하나를 고르세요!")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(pair[0]):
            st.session_state.winners.append(pair[0])
            st.session_state.pairs.pop(0)
            st.experimental_rerun()
    with col2:
        if st.button(pair[1]):
            st.session_state.winners.append(pair[1])
            st.session_state.pairs.pop(0)
            st.experimental_rerun()
else:
    # 라운드 종료 → 승자 모아 다음 라운드
    if len(st.session_state.winners) == 1:
        st.success(f"🎉 최종 결과: 이승민은 **{st.session_state.winners[0]}** 닮았어요! 🎉")
        if st.button("다시 하기"):
            for key in ["candidates", "round", "pairs", "winners"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()
    else:
        st.session_state.round += 1
        random.shuffle(st.session_state.winners)
        st.session_state.pairs = [
            st.session_state.winners[i:i+2]
            for i in range(0, len(st.session_state.winners), 2)
        ]
        st.session_state.candidates = st.session_state.winners.copy()
        st.session_state.winners = []
        st.experimental_rerun()
