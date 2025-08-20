import streamlit as st
st.set_page_config(page_title="이상형 월드컵", layout="centered")
st.title("이승민 이상형 월드컵")
import React, { useMemo, useRef, useState } from "react";

/**
 * 상원고 3학년 9반 이승민 동물상 이상형 월드컵
 * - 단일 파일 React 컴포넌트
 * - Tailwind 클래스로만 스타일링 (외부 라이브러리 X)
 * - 기본 이모지 동물 세트 + 사용자 이미지/이름 추가 지원
 * - 페어 매치 -> 라운드 진행 -> 최종 우승자 도출
 * - GitHub Pages에 올려도 바로 동작
 *
 * 사용법(요약):
 * 1) Vite + React 프로젝트에서 이 컴포넌트를 페이지에 import하여 렌더링하거나,
 * 2) CodeSandbox/StackBlitz에 React 템플릿 열고 붙여넣기,
 * 3) GitHub Pages로 배포하면 끝!
 */

// 타입 정의
type Candidate = {
  id: string;
  name: string;
  emoji?: string; // 기본 이모지 아이콘
  imgSrc?: string; // 사용자 업로드 이미지 (data URL)
};

function uid() {
  return Math.random().toString(36).slice(2);
}

function shuffle<T>(arr: T[]) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function chunkPairs<T>(arr: T[]): [T, T | null][] {
  const res: [T, T | null][] = [];
  for (let i = 0; i < arr.length; i += 2) {
    res.push([arr[i], arr[i + 1] ?? null]);
  }
  return res;
}

const DEFAULT_ANIMALS: Candidate[] = [
  { id: uid(), name: "강아지상", emoji: "🐶" },
  { id: uid(), name: "고양이상", emoji: "🐱" },
  { id: uid(), name: "여우상", emoji: "🦊" },
  { id: uid(), name: "호랑이상", emoji: "🐯" },
  { id: uid(), name: "사자상", emoji: "🦁" },
  { id: uid(), name: "곰돌이상", emoji: "🐻" },
  { id: uid(), name: "판다상", emoji: "🐼" },
  { id: uid(), name: "원숭이상", emoji: "🐵" },
  { id: uid(), name: "부엉이상", emoji: "🦉" },
  { id: uid(), name: "토끼상", emoji: "🐰" },
  { id: uid(), name: "개구리상", emoji: "🐸" },
  { id: uid(), name: "기린상", emoji: "🦒" },
];

function CandidateCard({ c, onClick }: { c: Candidate; onClick?: () => void }) {
  return (
    <button
      onClick={onClick}
      className="group flex-1 min-h-56 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow-md transition focus:outline-none focus:ring-2 focus:ring-indigo-400"
    >
      <div className="flex h-full flex-col items-center justify-center gap-3">
        <div className="text-6xl select-none">
          {c.imgSrc ? (
            <img
              src={c.imgSrc}
              alt={c.name}
              className="h-28 w-28 object-cover rounded-2xl border"
            />
          ) : (
            <span>{c.emoji ?? "🐾"}</span>
          )}
        </div>
        <div className="text-lg font-semibold text-gray-800">{c.name}</div>
      </div>
    </button>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return <h2 className="text-xl font-bold text-gray-900 mb-2">{children}</h2>;
}

export default function SeungminAnimalWorldcup() {
  const [title, setTitle] = useState(
    "상원고 3-9 이승민은 어떤 동물을 닮았을까? 월드컵"
  );
  const [editing, setEditing] = useState(true);
  const [cands, setCands] = useState<Candidate[]>(DEFAULT_ANIMALS);
  const [roundIndex, setRoundIndex] = useState(0); // 0부터 시작
  const [currentPairs, setCurrentPairs] = useState<[Candidate, Candidate | null][]>(
    []
  );
  const [winnersOfRound, setWinnersOfRound] = useState<Candidate[]>([]);
  const [champion, setChampion] = useState<Candidate | null>(null);
  const inputNameRef = useRef<HTMLInputElement>(null);
  const inputFileRef = useRef<HTMLInputElement>(null);

  const totalInitial = useMemo(() => cands.length, [cands.length]);

  function resetAll(shuffleFirst = true) {
    setChampion(null);
    setRoundIndex(0);
    const startPool = shuffleFirst ? shuffle(cands) : cands.slice();
    const pairs = chunkPairs(startPool);
    // bye 처리: 페어의 두 번째가 null이면 자동 승리
    const initialWinners: Candidate[] = [];
    const realPairs: [Candidate, Candidate | null][] = [];
    for (const [a, b] of pairs) {
      if (!b) initialWinners.push(a);
      else realPairs.push([a, b]);
    }
    setCurrentPairs(realPairs);
    setWinnersOfRound(initialWinners);
    setEditing(false);
  }

  function handlePickWinner(w: Candidate) {
    const nextPairs = currentPairs.slice();
    nextPairs.shift();

    const newWinners = [...winnersOfRound, w];

    if (nextPairs.length === 0) {
      // 라운드 종료 -> 다음 라운드 세팅
      if (newWinners.length === 1) {
        // 우승자 탄생
        setChampion(newWinners[0]);
        setCurrentPairs([]);
        setWinnersOfRound([]);
      } else {
        const nextPool = newWinners;
        const pairs = chunkPairs(nextPool);
        const nextInitialWinners: Candidate[] = [];
        const realPairs: [Candidate, Candidate | null][] = [];
        for (const [a, b] of pairs) {
          if (!b) nextInitialWinners.push(a);
          else realPairs.push([a, b]);
        }
        setRoundIndex((r) => r + 1);
        setCurrentPairs(realPairs);
        setWinnersOfRound(nextInitialWinners);
      }
    } else {
      setCurrentPairs(nextPairs);
      setWinnersOfRound(newWinners);
    }
  }

  function handleAddCandidateFromEmoji() {
    const name = inputNameRef.current?.value?.trim();
    if (!name) return;
    setCands((prev) => [...prev, { id: uid(), name, emoji: "🐾" }]);
    if (inputNameRef.current) inputNameRef.current.value = "";
  }

  function handleAddCandidateFromFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const nameRaw = inputNameRef.current?.value?.trim();
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      setCands((prev) => [
        ...prev,
        { id: uid(), name: nameRaw || file.name.replace(/\.[^.]+$/, ""), imgSrc: dataUrl },
      ]);
      if (inputNameRef.current) inputNameRef.current.value = "";
      if (inputFileRef.current) inputFileRef.current.value = "";
    };
    reader.readAsDataURL(file);
  }

  function handleRemoveCandidate(id: string) {
    setCands((prev) => prev.filter((c) => c.id !== id));
  }

  function handleShuffle() {
    setCands((prev) => shuffle(prev));
  }

  const roundSize = useMemo(() => {
    // 현재 라운드의 참가자 수 (자동승 포함)
    const participants = currentPairs.length * 2 + winnersOfRound.length;
    return participants || (champion ? 1 : cands.length);
  }, [currentPairs.length, winnersOfRound.length, champion, cands.length]);

  const progress = useMemo(() => {
    if (champion) return 100;
    const played = winnersOfRound.length; // 이번 라운드에서 확정된 승자 수 = 치른 매치 수
    const total = currentPairs.length + winnersOfRound.length; // 라운드에 포함된 총 매치 수
    if (total === 0) return 0;
    return Math.round((played / total) * 100);
  }, [currentPairs.length, winnersOfRound.length, champion]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 to-white text-gray-900 p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        <header className="mb-6 flex flex-col gap-2">
          <h1 className="text-2xl md:text-4xl font-extrabold leading-tight">
            {title}
          </h1>
          <p className="text-gray-600">
            \u2728 상원고 3학년 9반 전용 밈 프로젝트! 후보를 꾸미고 시작을 눌러 대결에서 더 닮은 동물을 골라 주세요.
          </p>
        </header>

        {editing ? (
          <div className="grid md:grid-cols-5 gap-6">
            <div className="md:col-span-3">
              <SectionTitle>후보 편집</SectionTitle>
              <div className="flex items-center gap-2 mb-3">
                <input
                  ref={inputNameRef}
                  placeholder="동물상 이름 (예: 수달상)"
                  className="flex-1 rounded-xl border px-3 py-2"
                />
                <button
                  onClick={handleAddCandidateFromEmoji}
                  className="rounded-xl px-3 py-2 border bg-white hover:bg-gray-50"
                >
                  이모지 추가
                </button>
                <label className="rounded-xl px-3 py-2 border bg-white hover:bg-gray-50 cursor-pointer">
                  이미지 추가
                  <input
                    ref={inputFileRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleAddCandidateFromFile}
                  />
                </label>
                <button
                  onClick={handleShuffle}
                  className="rounded-xl px-3 py-2 border bg-white hover:bg-gray-50"
                >
                  섞기
                </button>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {cands.map((c) => (
                  <div
                    key={c.id}
                    className="flex items-center justify-between gap-3 rounded-2xl border p-3 bg-white"
                  >
                    <div className="flex items-center gap-3">
                      <div className="text-2xl">
                        {c.imgSrc ? (
                          <img
                            src={c.imgSrc}
                            alt={c.name}
                            className="h-10 w-10 object-cover rounded-lg border"
                          />
                        ) : (
                          <span>{c.emoji ?? "🐾"}</span>
                        )}
                      </div>
                      <div className="font-medium">{c.name}</div>
                    </div>
                    <button
                      onClick={() => handleRemoveCandidate(c.id)}
                      className="text-sm text-red-600 hover:underline"
                    >
                      삭제
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="md:col-span-2">
              <SectionTitle>설정</SectionTitle>
              <label className="block text-sm text-gray-600 mb-1">제목</label>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full rounded-xl border px-3 py-2 mb-4"
              />

              <div className="rounded-2xl border bg-white p-4">
                <div className="text-sm text-gray-600 mb-3">
                  현재 후보 수: <b>{cands.length}</b>
                </div>
                <button
                  onClick={() => resetAll(true)}
                  className="w-full rounded-xl bg-indigo-600 text-white font-semibold py-3 hover:bg-indigo-700"
                  disabled={cands.length < 2}
                  title={cands.length < 2 ? "후보를 2개 이상 추가하세요" : "시작"}
                >
                  시작하기
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div>
            {!champion ? (
              <div>
                <div className="mb-4 flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    라운드 <b>{roundIndex + 1}</b> / 참가자 <b>{roundSize}</b>
                  </div>
                  <button
                    onClick={() => setEditing(true)}
                    className="text-sm rounded-xl px-3 py-2 border bg-white hover:bg-gray-50"
                  >
                    후보 편집으로 돌아가기
                  </button>
                </div>

                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-6">
                  <div
                    className="h-full bg-indigo-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                {currentPairs.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {currentPairs.length > 0 && (
                      <>
                        <CandidateCard
                          c={currentPairs[0][0]}
                          onClick={() => handlePickWinner(currentPairs[0][0])}
                        />
                        {currentPairs[0][1] ? (
                          <CandidateCard
                            c={currentPairs[0][1]!}
                            onClick={() => handlePickWinner(currentPairs[0][1]!)}
                          />
                        ) : (
                          <div className="rounded-2xl border p-4 flex items-center justify-center text-gray-500 bg-white">
                            부전승 처리됨
                          </div>
                        )}
                      </>
                    )}
                  </div>
                ) : (
                  <div className="text-center text-gray-600">다음 라운드를 준비 중...</div>
                )}
              </div>
            ) : (
              <div className="text-center">
                <div className="mx-auto max-w-md rounded-3xl border bg-white p-6 shadow-sm">
                  <div className="text-sm text-gray-600 mb-2">최종 결과</div>
                  <div className="text-4xl font-extrabold mb-3">우승자는 바로…</div>
                  <div className="flex items-center justify-center gap-4 mb-4">
                    <div className="text-7xl">
                      {champion.imgSrc ? (
                        <img
                          src={champion.imgSrc}
                          alt={champion.name}
                          className="h-24 w-24 object-cover rounded-2xl border"
                        />
                      ) : (
                        <span>{champion.emoji ?? "🐾"}</span>
                      )}
                    </div>
                    <div className="text-2xl font-bold">{champion.name}</div>
                  </div>

                  <div className="grid grid-cols-1 gap-2">
                    <button
                      onClick={() => {
                        setEditing(true);
                        setChampion(null);
                        setRoundIndex(0);
                        setCurrentPairs([]);
                        setWinnersOfRound([]);
                      }}
                      className="rounded-xl px-4 py-2 border bg-white hover:bg-gray-50"
                    >
                      후보 편집
                    </button>
                    <button
                      onClick={() => resetAll(true)}
                      className="rounded-xl px-4 py-2 bg-indigo-600 text-white font-semibold hover:bg-indigo-700"
                    >
                      같은 후보로 다시 하기
                    </button>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(
                          `이승민 동물상 월드컵 결과: ${champion.name}! (${title})`
                        );
                        alert("결과 문구를 클립보드에 복사했어요!");
                      }}
                      className="rounded-xl px-4 py-2 border bg-white hover:bg-gray-50"
                    >
                      결과 문구 복사하기
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        <footer className="mt-10 text-xs text-gray-500">
          Made for 3-9 Seungmin · \u00A9 {new Date().getFullYear()} 월드컵 생성기
        </footer>
      </div>
    </div>
  );
}
