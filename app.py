import json
from pathlib import Path

import streamlit as st


LEGACY_QUESTIONS = [
    {
        "question": "次のうち、一般的にブランド品の査定で最初に確認する情報はどれですか？",
        "genre": "ブランド品",
        "difficulty": "初級（基礎用語・刻印）",
        "choices": {
            "A": "ブランド名・モデル名・付属品の有無",
            "B": "購入者の好きな色",
            "C": "店舗からの距離だけ",
            "D": "商品の写真の枚数だけ",
        },
        "answer": "A",
        "explanation": "ブランド名やモデル名は相場を確認するための基本情報です。箱・保証書などの付属品も査定額に影響するため、あわせて確認します。",
    },
    {
        "question": "ブランド品の査定で、同じシリーズでもモデル名を確認する理由はどれですか？",
        "genre": "ブランド品",
        "difficulty": "中級（モデル名・素材）",
        "choices": {
            "A": "モデルごとに相場や仕様が異なるため",
            "B": "モデル名で商品の重さが決まるため",
            "C": "モデル名が長いほど高価になるため",
            "D": "モデル名だけで真贋が確定するため",
        },
        "answer": "A",
        "explanation": "同じブランドやシリーズでも、モデル、サイズ、素材、発売時期によって相場や仕様が異なります。モデル名の確認は適切な査定の基本です。",
    },
    {
        "question": "金製品の品位を表す「K18」は、一般に何を意味しますか？",
        "genre": "貴金属",
        "difficulty": "初級（基礎用語・刻印）",
        "choices": {
            "A": "純度が約18%の金",
            "B": "純度が約75%の金",
            "C": "重さが18グラムの金",
            "D": "18年前に製造された金",
        },
        "answer": "B",
        "explanation": "K18は24分率で18を示すため、金の純度は約75%です。残りは銀や銅などの金属で、強度や色味を調整しています。",
    },
    {
        "question": "お客様から貴金属をお預かりした際、査定前に特に大切な対応はどれですか？",
        "genre": "貴金属",
        "difficulty": "中級（モデル名・素材）",
        "choices": {
            "A": "重量や刻印を確認し、状態を丁寧に記録する",
            "B": "すぐに磨いて傷を見えなくする",
            "C": "刻印を削って確認しやすくする",
            "D": "お客様の目の前で分解する",
        },
        "answer": "A",
        "explanation": "重量、刻印、石の有無、傷や破損などを丁寧に確認・記録することが、適切で透明性のある査定につながります。",
    },
    {
        "question": "骨とう品の査定で、作品の価値を判断する手がかりとして重要なものはどれですか？",
        "genre": "骨とう品・時計",
        "difficulty": "上級（真贋・レア査定）",
        "choices": {
            "A": "作者の署名や provenance（来歴）、保存状態",
            "B": "商品の箱の色だけ",
            "C": "持ち主の購入時の気分",
            "D": "写真を撮った時間帯",
        },
        "answer": "A",
        "explanation": "骨とう品は作者や年代、来歴、保存状態などが価値に影響します。複数の情報を照合し、真贋を慎重に確認することが重要です。",
    },
    {
        "question": "高級時計のレア査定で、通常の動作確認に加えて確認したいものはどれですか？",
        "genre": "骨とう品・時計",
        "difficulty": "上級（真贋・レア査定）",
        "choices": {
            "A": "リファレンス番号、製造年、交換部品の履歴",
            "B": "ベルトの長さだけ",
            "C": "文字盤の写真の明るさだけ",
            "D": "購入店舗の内装",
        },
        "answer": "A",
        "explanation": "高級時計はリファレンス番号や製造年、部品交換の履歴が、真贋や希少性、査定額に関わります。付属品や整備履歴も確認します。",
    },
]


def load_questions() -> list[dict]:
    questions_path = Path(__file__).with_name("questions.json")
    with questions_path.open(encoding="utf-8-sig") as file:
        return json.load(file)


QUESTIONS = load_questions()


def initialize_session_state() -> None:
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "last_is_correct" not in st.session_state:
        st.session_state.last_is_correct = False
    if "incorrect_questions" not in st.session_state:
        st.session_state.incorrect_questions = []


def reset_quiz() -> None:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_is_correct = False
    st.session_state.incorrect_questions = []


st.set_page_config(page_title="買取営業クイズ", page_icon="💡", layout="centered")
st.markdown(
    """
    <style>
    :root {
        --ink: #26332f;
        --muted: #68716d;
        --paper: #f5f2ec;
        --panel: #fffdf9;
        --bronze: #a9793f;
        --bronze-dark: #80592f;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] .main {
        background: var(--paper);
    }

    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: 0;
    }

    h1 {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    [data-testid="stSidebar"] {
        background: var(--ink);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #f7f3eb;
    }

    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid #e5ded2;
        border-left: 4px solid var(--bronze);
        border-radius: 8px;
        padding: 0.75rem 1rem;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--ink);
    }

    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label p {
        color: var(--ink) !important;
    }

    [data-testid="stProgress"] > div > div > div {
        background-color: var(--bronze);
    }

    div[data-testid="stAlert"] {
        border-radius: 8px;
        border-width: 1px;
    }

    button[kind="primary"] {
        background: var(--bronze-dark);
        border-color: var(--bronze-dark);
    }

    button[kind="primary"]:hover {
        background: #674724;
        border-color: #674724;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
initialize_session_state()

st.title("買取営業クイズ")
st.caption("ブランド・貴金属の基礎知識を確認しましょう")

genre_options = ["すべて", "ブランド品", "貴金属", "骨とう品・時計"]
difficulty_options = [
    "初級（基礎用語・刻印）",
    "中級（モデル名・素材）",
    "上級（真贋・レア査定）",
]
difficulty_values = {
    "初級（基礎用語・刻印）": "初級",
    "中級（モデル名・素材）": "中級",
    "上級（真贋・レア査定）": "上級",
}

with st.sidebar:
    st.header("出題条件")
    selected_genre = st.selectbox("ジャンル", genre_options)
    selected_difficulty = st.selectbox("難易度", difficulty_options)

filter_signature = (selected_genre, selected_difficulty)
if st.session_state.get("filter_signature") != filter_signature:
    reset_quiz()
    st.session_state.filter_signature = filter_signature

selected_categories = {
    "すべて": {"ブランド品", "貴金属", "骨とう品", "腕時計"},
    "ブランド品": {"ブランド品"},
    "貴金属": {"貴金属"},
    "骨とう品・時計": {"骨とう品", "腕時計"},
}[selected_genre]

filtered_questions = [
    question
    for question in QUESTIONS
    if question["category"] in selected_categories
    and question["level"] == difficulty_values[selected_difficulty]
]

total_questions = len(filtered_questions)
if total_questions == 0:
    st.warning("選択された条件に一致する問題がありません。別の条件を選択してください。")
    st.stop()

current_index = st.session_state.current_question

if current_index >= total_questions:
    accuracy = round(st.session_state.score / total_questions * 100)
    st.success("クイズ終了！")
    st.header("最終結果")
    st.metric("正解率", f"{accuracy}% 正解！")
    st.write(f"正解数: **{st.session_state.score} / {total_questions}問**")

    if accuracy == 100:
        st.success("全問正解です！素晴らしい成果です。")
    elif accuracy >= 80:
        st.success("とても良い結果です。間違えた問題を復習して知識を定着させましょう。")
    elif accuracy >= 60:
        st.warning("基礎は身についています。復習リストで苦手分野を確認しましょう。")
    else:
        st.info("まずは復習リストを確認し、もう一度挑戦して知識を身につけましょう。")

    st.subheader("復習リスト")
    if st.session_state.incorrect_questions:
        st.write(f"今回間違えた問題: **{len(st.session_state.incorrect_questions)}問**")
        for review_index, review in enumerate(st.session_state.incorrect_questions, start=1):
            with st.expander(f"{review_index}. {review['question']}"):
                st.write(f"あなたの回答: **{review['selected_answer']}**")
                st.write(f"正解: **{review['answer']}**")
                st.info(f"**解説:** {review['explanation']}")
    else:
        st.success("間違えた問題はありません。全問正解です！")

    st.progress(1.0)
    if st.button("もう一度挑戦する", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()
    st.stop()

question = filtered_questions[current_index]
score_col, progress_col = st.columns(2)
score_col.metric("正解数", f"{st.session_state.score}問")
progress_col.metric("進捗", f"{current_index + 1} / {total_questions}問目")
st.progress((current_index + 1) / total_questions)

with st.container(border=True):
    st.caption(f"ジャンル: {question['category']}　｜　難易度: {question['level']}")
    st.subheader(question["question"])

    choice_labels = [f"{index}. {option}" for index, option in enumerate(question["options"], start=1)]
    selected_label = st.radio(
        "選択肢を1つ選んでください",
        choice_labels,
        key=f"selected_answer_{selected_genre}_{selected_difficulty}_{current_index}",
        disabled=st.session_state.answered,
    )
    selected_answer = selected_label.split(". ", 1)[1]

if not st.session_state.answered:
    if st.button("回答する", type="primary", use_container_width=True):
        st.session_state.last_is_correct = selected_answer == question["answer"]
        if st.session_state.last_is_correct:
            st.session_state.score += 1
        else:
            st.session_state.incorrect_questions.append(
                {
                    "question": question["question"],
                    "selected_answer": selected_answer,
                    "answer": question["answer"],
                    "explanation": question["explanation"],
                }
            )
        st.session_state.answered = True
        st.rerun()
else:
    if st.session_state.last_is_correct:
        st.success("正解です！")
    else:
        st.error(f"不正解です。正解は「{question['answer']}」です。")

    st.info(f"**解説:** {question['explanation']}")

    if st.button("次の問題へ", type="primary", use_container_width=True):
        st.session_state.current_question += 1
        st.session_state.answered = False
        st.session_state.last_is_correct = False
        st.rerun()
