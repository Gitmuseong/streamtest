import streamlit as st
st.set_page_config(page_title="이상형 월드컵", layout="centered")
st.title("이승민 이상형 월드컵")
import random

st.set_page_config(page_title="이승민 동물상 이상형 월드컵", page_icon="🐾", layout="centered")

# 초기 후보 (이모지 기반 동물상)
DEFAULT_ANIMALS = [
    "🐶 강아지상",
    "🐱 고양이상",
    "🦊 여우상",
    "🐯 호랑이상",
    "🦁 사자상",
    "🐻 곰돌이상",
    "🐼 판다상",
    "🐵 원숭이상",
    "🦉 부엉이상",
    "🐰 토끼상",
    "🐸 개구리상",
    "🦒 기린상",
]

# 세션 상태 초기화
if "candidates" not in st.session_state:
    st.session_state.candidates = random.sample(DEFAULT_ANIMALS, len(DEFAULT_ANIMALS))
if "round" not in st.session_state:
    st.session_state.round = 1
if "pairs" not in st.session_state:
    st.session_state.pairs = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "champion" not in st.session_state:
    st.session_state.champion = None

def make_pairs(lst):
    pairs = []
    for i in range(0, len(lst), 2):
        if i + 1 < len(lst):
            pairs.append((lst[i], lst[i+1]))
        else:  # 홀수면 부전승 처리
            st.session_state.winners.append(lst[i])
    return pairs

# 첫 라운드 세팅
if not st.session_state.pairs and not st.session_state.champion:
    st.session_state.pairs = make_pairs(st.session_state.candidates)

st.title("🐾 상원고 3-9 이승민은 어떤 동물을 닮았을까? 🐾")
st.subheader(f"Round {st.session_state.round}")

# 우승자가 정해졌는지 확인
if st.session_state.champion:
    st.success(f"최종 우승자는... {st.session_state.champion} 🎉")
    if st.button("다시 시작하기"):
        for key in ["candidates", "round", "pairs", "winners", "champion"]:
            if key in st.session_state:
                del st.session_state[key]
    st.stop()

# 현재 매치 보여주기
if st.session_state.pairs:
    a, b = st.session_state.pairs[0]
    col1, col2 = st.columns(2)
    with col1:
        if st.button(a, use_container_width=True):
            st.session_state.winners.append(a)
            st.session_state.pairs.pop(0)
            st.rerun()
    with col2:
        if st.button(b, use_container_width=True):
            st.session_state.winners.append(b)
            st.session_state.pairs.pop(0)
            st.rerun()
else:
    # 라운드 종료 후 다음 라운드 세팅
    if len(st.session_state.winners) == 1:
        st.session_state.champion = st.session_state.winners[0]
    else:
        st.session_state.candidates = st.session_state.winners
        st.session_state.winners = []
        st.session_state.pairs = make_pairs(st.session_state.candidates)
        st.session_state.round += 1
    st.rerun()
