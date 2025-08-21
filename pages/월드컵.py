import streamlit as st
import random

st.set_page_config(page_title="동물 월드컵", page_icon="🐾", layout="centered")

# --- 세션 상태 초기화 ---
if "candidates" not in st.session_state:
    st.session_state.candidates = ["강아지 🐶", "고양이 🐱", "판다 🐼", "여우 🦊", "호랑이 🐯", "토끼 🐰", "부엉이 🦉", "코끼리 🐘"]
    random.shuffle(st.session_state.candidates)
if "round" not in st.session_state:
    st.session_state.round = 1
if "pairs" not in st.session_state:
    st.session_state.pairs = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("🐾 상원고 3학년 9반 이승민은 어떤 동물을 닮았을까? 월드컵")

# --- 게임 진행 함수 ---
def make_pairs():
    cands = st.session_state.candidates
    pairs = []
    for i in range(0, len(cands), 2):
        if i + 1 < len(cands):
            pairs.append((cands[i], cands[i + 1]))
        else:
            # 홀수일 경우 자동 진출
            pairs.append((cands[i], None))
    st.session_state.pairs = pairs
    st.session_state.winners = []

def next_round():
    st.session_state.candidates = st.session_state.winners
    st.session_state.round += 1
    if len(st.session_state.candidates) == 1:
        st.session_state.finished = True
    else:
        make_pairs()

# --- 게임 로직 ---
if not st.session_state.finished:
    if not st.session_state.pairs:
        make_pairs()

    st.subheader(f"Round {st.session_state.round} - {len(st.session_state.candidates)}강")

    for idx, (a, b) in enumerate(st.session_state.pairs):
        cols = st.columns(2)
        with cols[0]:
            if st.button(a, key=f"{st.session_state.round}_{idx}_a"):
                st.session_state.winners.append(a)
                if b and b not in st.session_state.winners:
                    pass
                if len(st.session_state.winners) == len(st.session_state.pairs):
                    next_round()
                st.experimental_rerun()
        with cols[1]:
            if b:
                if st.button(b, key=f"{st.session_state.round}_{idx}_b"):
                    st.session_state.winners.append(b)
                    if a and a not in st.session_state.winners:
                        pass
                    if len(st.session_state.winners) == len(st.session_state.pairs):
                        next_round()
                    st.experimental_rerun()
            else:
                st.markdown("자동 진출 🚀")
                st.session_state.winners.append(a)
                if len(st.session_state.winners) == len(st.session_state.pairs):
                    next_round()
                st.experimental_rerun()
else:
    st.success(f"🎉 최종 결과! 이승민은 **{st.session_state.candidates[0]}** 닮았다구 생각돼! 🏆")
    if st.button("다시 하기 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
