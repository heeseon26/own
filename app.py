# -*- coding: utf-8 -*-
from __future__ import annotations

import html
import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


# ─────────────────────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OWM Influencer Desk",
    page_icon="◡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

KST = ZoneInfo("Asia/Seoul")
LOGO_B64 = "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"

REQUIRED_RESPONSE_COLUMNS = [
    "기프트 수령",
    "응대 완료",
    "응대직원",
    "응대일시",
    "응대메모",
]

COLUMN_ALIASES = {
    "date": ["협찬일", "방문일", "날짜"],
    "time": ["방문 시간", "방문시간", "시간"],
    "country": ["국가", "언어권"],
    "account": ["계정주소", "계정 주소", "SNS", "인스타그램", "인스타 주소"],
    "name": ["방문자명", "인플루언서명", "이름"],
    "phone": ["연락처", "전화번호", "휴대폰"],
    "shoot": ["촬영 유형 선택/가이드", "촬영 유형", "촬영유형", "가이드"],
    "gift": ["기프트", "증정 제품", "증정품"],
    "amount": ["유료금액", "유료 금액", "금액"],
    "note": ["비고", "메모", "주의사항"],
    "gift_received": ["기프트 수령", "기프트수령"],
    "responded": ["응대 완료", "응대완료"],
    "staff": ["응대직원", "응대 직원"],
    "responded_at": ["응대일시", "응대 일시"],
    "response_note": ["응대메모", "응대 메모"],
}


# ─────────────────────────────────────────────────────────────
# 디자인
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        :root {
            --owm-bg: #f4f1ec;
            --owm-card: #ffffff;
            --owm-ink: #222222;
            --owm-muted: #77716a;
            --owm-line: #e8e2da;
            --owm-dark: #222222;
            --owm-soft: #faf8f5;
            --owm-pink: #d87996;
            --owm-pink-soft: #fff0f4;
            --owm-green: #66806c;
        }

        html, body, [class*="css"] {
            font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI",
                         "Noto Sans KR", sans-serif;
        }

        #MainMenu,
        header,
        footer,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 88% 2%, rgba(216,121,150,.10), transparent 24rem),
                var(--owm-bg);
        }

        [data-testid="stMain"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding: 2.2rem 2rem 5rem !important;
        }

        .owm-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .owm-brand {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .owm-logo-box {
            width: 96px;
            height: 72px;
            padding: 12px 16px;
            border-radius: 20px;
            display: grid;
            place-items: center;
            background: var(--owm-dark);
            box-shadow: 0 16px 38px rgba(34,34,34,.16);
        }

        .owm-logo-box img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .owm-title {
            margin: 0;
            color: var(--owm-ink);
            font-size: 1.55rem;
            line-height: 1.15;
            letter-spacing: -.035em;
            font-weight: 850;
        }

        .owm-subtitle {
            margin-top: .35rem;
            color: var(--owm-muted);
            font-size: .82rem;
            letter-spacing: .04em;
        }

        .owm-live {
            display: inline-flex;
            align-items: center;
            gap: .48rem;
            padding: .62rem .85rem;
            border: 1px solid var(--owm-line);
            border-radius: 999px;
            background: rgba(255,255,255,.72);
            color: var(--owm-muted);
            font-size: .76rem;
            font-weight: 750;
            white-space: nowrap;
            backdrop-filter: blur(10px);
        }

        .owm-live-dot {
            width: .52rem;
            height: .52rem;
            border-radius: 50%;
            background: var(--owm-green);
            box-shadow: 0 0 0 4px rgba(102,128,108,.12);
        }

        .owm-hero {
            padding: 2rem 2.1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,.7);
            border-radius: 28px;
            background:
                linear-gradient(125deg, rgba(34,34,34,.98), rgba(48,46,44,.95));
            color: white;
            box-shadow: 0 24px 55px rgba(37,32,28,.13);
        }

        .owm-eyebrow {
            color: #d9d3cc;
            font-size: .74rem;
            font-weight: 750;
            letter-spacing: .15em;
            text-transform: uppercase;
        }

        .owm-hero h1 {
            margin: .7rem 0 .55rem;
            color: white;
            font-size: clamp(2rem, 4vw, 3.35rem);
            line-height: 1.04;
            letter-spacing: -.055em;
            font-weight: 850;
        }

        .owm-hero p {
            margin: 0;
            max-width: 690px;
            color: #d5d1cc;
            font-size: .96rem;
            line-height: 1.7;
        }

        .owm-metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0,1fr));
            gap: 1rem;
            margin: 1rem 0 1.5rem;
        }

        .owm-metric {
            padding: 1.25rem 1.35rem;
            border: 1px solid var(--owm-line);
            border-radius: 22px;
            background: rgba(255,255,255,.86);
            box-shadow: 0 12px 34px rgba(38,32,28,.055);
            backdrop-filter: blur(10px);
        }

        .owm-metric-label {
            color: var(--owm-muted);
            font-size: .76rem;
            font-weight: 750;
        }

        .owm-metric-value {
            margin-top: .45rem;
            color: var(--owm-ink);
            font-size: 2rem;
            line-height: 1;
            font-weight: 850;
            letter-spacing: -.045em;
        }

        .owm-section-head {
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 1rem;
            margin: 2rem 0 .9rem;
        }

        .owm-section-title {
            color: var(--owm-ink);
            font-size: 1.25rem;
            font-weight: 850;
            letter-spacing: -.03em;
        }

        .owm-section-copy {
            margin-top: .28rem;
            color: var(--owm-muted);
            font-size: .82rem;
        }

        .owm-count {
            color: var(--owm-muted);
            font-size: .76rem;
            font-weight: 700;
        }

        div[data-testid="stTextInput"] input {
            min-height: 3.35rem;
            padding: 0 1.05rem;
            border: 1px solid var(--owm-line);
            border-radius: 17px;
            background: rgba(255,255,255,.92);
            color: var(--owm-ink);
            font-size: .98rem;
            box-shadow: 0 10px 28px rgba(38,32,28,.045);
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: rgba(216,121,150,.75);
            box-shadow: 0 0 0 4px rgba(216,121,150,.11);
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--owm-line) !important;
            border-radius: 24px !important;
            background: rgba(255,255,255,.93) !important;
            box-shadow: 0 13px 38px rgba(38,32,28,.055) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: .25rem !important;
        }

        .owm-visitor-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .owm-name {
            color: var(--owm-ink);
            font-size: 1.18rem;
            font-weight: 850;
            letter-spacing: -.025em;
        }

        .owm-account {
            display: block;
            max-width: 720px;
            margin-top: .28rem;
            overflow: hidden;
            color: var(--owm-muted);
            font-size: .8rem;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .owm-badge {
            display: inline-flex;
            align-items: center;
            padding: .42rem .68rem;
            border-radius: 999px;
            font-size: .7rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .owm-badge.pending {
            color: #8c5570;
            background: var(--owm-pink-soft);
        }

        .owm-badge.done {
            color: #4f7058;
            background: #edf5ef;
        }

        .owm-detail-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: .7rem;
        }

        .owm-detail {
            min-width: 0;
            padding: .82rem .9rem;
            border-radius: 15px;
            background: var(--owm-soft);
        }

        .owm-detail-label {
            margin-bottom: .34rem;
            color: #8b847d;
            font-size: .68rem;
            font-weight: 750;
        }

        .owm-detail-value {
            overflow: hidden;
            color: #3b3835;
            font-size: .82rem;
            font-weight: 720;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .owm-note {
            margin-top: .75rem;
            padding: .85rem .95rem;
            border-radius: 15px;
            background: #fff7f9;
            color: #744d5b;
            font-size: .79rem;
            line-height: 1.6;
        }

        .owm-done-strip {
            margin-top: .8rem;
            padding: .82rem .95rem;
            border: 1px solid #dfeae2;
            border-radius: 15px;
            background: #f3f8f4;
            color: #516b57;
            font-size: .78rem;
            line-height: 1.55;
        }

        .owm-empty {
            padding: 3.2rem 1.5rem;
            border: 1px dashed #d7cfc5;
            border-radius: 24px;
            background: rgba(255,255,255,.58);
            color: var(--owm-muted);
            text-align: center;
        }

        .owm-empty-mark {
            width: 44px;
            height: 44px;
            display: grid;
            place-items: center;
            margin: 0 auto .8rem;
            border-radius: 14px;
            background: var(--owm-pink-soft);
            color: var(--owm-pink);
            font-size: 1.25rem;
            font-weight: 850;
        }

        .owm-empty strong {
            display: block;
            margin-bottom: .35rem;
            color: var(--owm-ink);
            font-size: .96rem;
        }

        div.stButton > button {
            min-height: 2.9rem;
            border-radius: 14px;
            border: 1px solid var(--owm-line);
            font-weight: 800;
            transition: transform .15s ease, box-shadow .15s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-1px);
            border-color: #d8cfc5;
            box-shadow: 0 9px 20px rgba(38,32,28,.08);
        }

        div.stButton > button[kind="primary"] {
            border-color: var(--owm-dark);
            background: var(--owm-dark);
            color: white;
        }

        div[data-testid="stCheckbox"] label p,
        div[data-testid="stTextArea"] label p,
        div[data-testid="stTextInput"] label p {
            color: #5c5752;
            font-size: .79rem;
            font-weight: 750;
        }

        div[data-testid="stTextArea"] textarea {
            border: 1px solid var(--owm-line);
            border-radius: 14px;
        }

        div[role="dialog"] {
            border-radius: 24px !important;
        }

        .owm-footer {
            margin-top: 2.5rem;
            color: #9a938b;
            font-size: .7rem;
            text-align: center;
        }

        @media (max-width: 900px) {
            .block-container {
                padding: 1.35rem 1rem 3.5rem !important;
            }

            .owm-header {
                align-items: flex-start;
            }

            .owm-logo-box {
                width: 82px;
                height: 62px;
            }

            .owm-metric-grid {
                grid-template-columns: 1fr;
            }

            .owm-detail-grid {
                grid-template-columns: repeat(2, minmax(0,1fr));
            }
        }

        @media (max-width: 600px) {
            .owm-header {
                flex-direction: column;
            }

            .owm-hero {
                padding: 1.55rem 1.35rem;
                border-radius: 22px;
            }

            .owm-detail-grid {
                grid-template-columns: 1fr;
            }

            .owm-visitor-top {
                flex-direction: column;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# 데이터 연결
# ─────────────────────────────────────────────────────────────
def has_sheet_config() -> bool:
    try:
        return (
            "gcp_service_account" in st.secrets
            and "sheet" in st.secrets
            and bool(st.secrets["sheet"].get("spreadsheet_id"))
        )
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def get_worksheet():
    if not has_sheet_config():
        return None

    if gspread is None or Credentials is None:
        raise RuntimeError("Google Sheets 연결 패키지가 설치되지 않았습니다.")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=scopes,
    )
    client = gspread.authorize(credentials)

    sheet_id = st.secrets["sheet"]["spreadsheet_id"]
    worksheet_name = st.secrets["sheet"].get("worksheet_name", "인플루언서")
    return client.open_by_key(sheet_id).worksheet(worksheet_name)


def ensure_response_columns(worksheet) -> list[str]:
    headers = [str(v).strip() for v in worksheet.row_values(1)]
    missing = [name for name in REQUIRED_RESPONSE_COLUMNS if name not in headers]

    if missing:
        headers.extend(missing)
        worksheet.update(range_name="A1", values=[headers])

    return headers


@st.cache_data(ttl=20, show_spinner=False)
def load_sheet_records() -> pd.DataFrame:
    worksheet = get_worksheet()
    if worksheet is None:
        return pd.DataFrame()

    headers = ensure_response_columns(worksheet)
    values = worksheet.get_all_values()

    if len(values) <= 1:
        return pd.DataFrame(columns=headers + ["_sheet_row"])

    rows = []
    for raw_row in values[1:]:
        padded = raw_row + [""] * max(0, len(headers) - len(raw_row))
        rows.append(padded[: len(headers)])

    frame = pd.DataFrame(rows, columns=headers)
    frame["_sheet_row"] = range(2, len(frame) + 2)
    return frame


def preview_records() -> pd.DataFrame:
    today = datetime.now(KST).strftime("%Y-%m-%d")
    rows = [
        {
            "협찬일": today,
            "방문 시간": "14:00",
            "국가": "영어권",
            "계정주소": "https://www.instagram.com/owm_preview",
            "방문자명": "OWM Preview",
            "연락처": "010-0000-0000",
            "촬영 유형 선택/가이드": "에피미러 X OWM",
            "기프트": "REJU-ECTO · JUVE-ECTO",
            "유료금액": "450000",
            "비고": "구글시트 연결 전 화면 확인용 예시입니다.",
            "기프트 수령": "",
            "응대 완료": "",
            "응대직원": "",
            "응대일시": "",
            "응대메모": "",
            "_sheet_row": 2,
        },
        {
            "협찬일": today,
            "방문 시간": "16:30",
            "국가": "중국",
            "계정주소": "https://www.instagram.com/owm_guest",
            "방문자명": "Guest Creator",
            "연락처": "010-1111-2222",
            "촬영 유형 선택/가이드": "레비오 X OWM",
            "기프트": "PDRN 크림",
            "유료금액": "",
            "비고": "",
            "기프트 수령": "TRUE",
            "응대 완료": "TRUE",
            "응대직원": "직원 예시",
            "응대일시": f"{today} 11:20",
            "응대메모": "",
            "_sheet_row": 3,
        },
    ]
    return pd.DataFrame(rows)


def get_records() -> tuple[pd.DataFrame, bool, str]:
    if has_sheet_config():
        try:
            return load_sheet_records(), True, ""
        except Exception as exc:
            return pd.DataFrame(), False, str(exc)

    if "preview_df" not in st.session_state:
        st.session_state.preview_df = preview_records()

    return st.session_state.preview_df.copy(), False, ""


def resolve_columns(columns: list[str]) -> dict[str, str | None]:
    resolved: dict[str, str | None] = {}
    normalized = {str(col).strip(): str(col) for col in columns}

    for key, aliases in COLUMN_ALIASES.items():
        resolved[key] = next(
            (normalized[alias] for alias in aliases if alias in normalized),
            None,
        )

    return resolved


def value_of(row: pd.Series, columns: dict[str, str | None], key: str) -> str:
    column = columns.get(key)
    if not column:
        return ""

    value = row.get(column, "")
    if pd.isna(value):
        return ""

    return str(value).strip()


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
        "o",
        "예",
        "완료",
        "⭕",
        "checked",
    }


def date_key(value: str) -> str:
    text = str(value).strip()
    if not text:
        return ""

    text = text.replace("년", "-").replace("월", "-").replace("일", "")
    text = re.sub(r"[./]", "-", text)
    text = re.sub(r"\s+", "", text)

    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return ""

    return parsed.strftime("%Y-%m-%d")


def format_money(value: str) -> str:
    text = str(value).strip().replace(",", "").replace("₩", "").replace("원", "")
    if not text:
        return "-"

    try:
        return f"₩{int(float(text)):,}"
    except ValueError:
        return html.escape(str(value))


def safe(value: Any, fallback: str = "-") -> str:
    text = str(value).strip() if value is not None else ""
    return html.escape(text or fallback)


def update_sheet_response(
    sheet_row: int,
    staff_name: str,
    gift_received: bool,
    response_note: str,
) -> None:
    worksheet = get_worksheet()
    if worksheet is None:
        raise RuntimeError("Google Sheets가 연결되지 않았습니다.")

    headers = ensure_response_columns(worksheet)
    timestamp = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    updates = {
        "기프트 수령": "TRUE" if gift_received else "FALSE",
        "응대 완료": "TRUE",
        "응대직원": staff_name.strip(),
        "응대일시": timestamp,
        "응대메모": response_note.strip(),
    }

    for header, value in updates.items():
        column_index = headers.index(header) + 1
        worksheet.update_cell(int(sheet_row), column_index, value)

    load_sheet_records.clear()


def update_preview_response(
    sheet_row: int,
    staff_name: str,
    gift_received: bool,
    response_note: str,
) -> None:
    frame = st.session_state.preview_df.copy()
    mask = frame["_sheet_row"].astype(int) == int(sheet_row)

    frame.loc[mask, "기프트 수령"] = "TRUE" if gift_received else "FALSE"
    frame.loc[mask, "응대 완료"] = "TRUE"
    frame.loc[mask, "응대직원"] = staff_name.strip()
    frame.loc[mask, "응대일시"] = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    frame.loc[mask, "응대메모"] = response_note.strip()

    st.session_state.preview_df = frame


# ─────────────────────────────────────────────────────────────
# 응대 완료 모달
# ─────────────────────────────────────────────────────────────
@st.dialog("응대 완료", width="small")
def response_dialog(
    sheet_row: int,
    visitor_name: str,
    live_mode: bool,
) -> None:
    st.markdown(
        f"**{html.escape(visitor_name)}** 님의 응대 완료 기록을 남깁니다."
    )

    with st.form(f"response_form_{sheet_row}", clear_on_submit=False):
        staff_name = st.text_input(
            "응대직원",
            placeholder="응대한 직원 이름",
        )
        gift_received = st.checkbox(
            "기프트 수령 완료",
            value=True,
        )
        response_note = st.text_area(
            "응대 메모",
            placeholder="전달사항이 있을 때만 입력하세요.",
            height=90,
        )
        submitted = st.form_submit_button(
            "응대 완료 저장",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not staff_name.strip():
            st.error("응대직원 이름을 입력해주세요.")
            return

        try:
            if live_mode:
                update_sheet_response(
                    sheet_row,
                    staff_name,
                    gift_received,
                    response_note,
                )
            else:
                update_preview_response(
                    sheet_row,
                    staff_name,
                    gift_received,
                    response_note,
                )

            st.toast("응대 완료로 표시했습니다.", icon="✓")
            st.rerun()

        except Exception as exc:
            st.error(f"저장하지 못했습니다. 관리자에게 확인해주세요.\n\n{exc}")


# ─────────────────────────────────────────────────────────────
# 화면
# ─────────────────────────────────────────────────────────────
records, live_mode, connection_error = get_records()
columns = resolve_columns(list(records.columns))

today = datetime.now(KST).strftime("%Y-%m-%d")
today_label = datetime.now(KST).strftime("%Y년 %m월 %d일")

if not records.empty and columns.get("date"):
    today_mask = records[columns["date"]].map(date_key) == today
else:
    today_mask = pd.Series(False, index=records.index)

if not records.empty and columns.get("responded"):
    done_mask = records[columns["responded"]].map(truthy)
else:
    done_mask = pd.Series(False, index=records.index)

today_records = records[today_mask].copy() if not records.empty else records.copy()
today_total = int(today_mask.sum()) if len(today_mask) else 0
today_done = int((today_mask & done_mask).sum()) if len(today_mask) else 0
today_pending = max(today_total - today_done, 0)

connection_label = "GOOGLE SHEET CONNECTED" if live_mode else "PREVIEW MODE"

st.markdown(
    f"""
    <div class="owm-header">
        <div class="owm-brand">
            <div class="owm-logo-box">
                <img src="data:image/png;base64,{LOGO_B64}" alt="OWM">
            </div>
            <div>
                <div class="owm-title">Influencer Desk</div>
                <div class="owm-subtitle">OPTIMA WELLNESS · SINSA</div>
            </div>
        </div>
        <div class="owm-live">
            <span class="owm-live-dot"></span>
            {connection_label}
        </div>
    </div>

    <div class="owm-hero">
        <div class="owm-eyebrow">{today_label}</div>
        <h1>오늘 방문자를<br>빠르게 확인하세요.</h1>
        <p>
            준비된 명단에서 정보를 확인한 뒤,
            응대한 직원은 <b>응대 완료</b>만 표시하면 됩니다.
        </p>
    </div>

    <div class="owm-metric-grid">
        <div class="owm-metric">
            <div class="owm-metric-label">오늘 방문 예정</div>
            <div class="owm-metric-value">{today_total}</div>
        </div>
        <div class="owm-metric">
            <div class="owm-metric-label">응대 완료</div>
            <div class="owm-metric-value">{today_done}</div>
        </div>
        <div class="owm-metric">
            <div class="owm-metric-label">응대 대기</div>
            <div class="owm-metric-value">{today_pending}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if connection_error:
    st.error(
        "Google Sheets 연결에 실패했습니다. "
        "시트 공유 권한과 Streamlit Secrets를 확인해주세요."
    )

search_query = st.text_input(
    "방문자 검색",
    placeholder="이름 · 인스타 계정 · 연락처로 검색",
    label_visibility="collapsed",
)

search_query = search_query.strip().lower()

if search_query:
    searchable_columns = [
        columns.get("name"),
        columns.get("account"),
        columns.get("phone"),
        columns.get("country"),
    ]
    searchable_columns = [col for col in searchable_columns if col]

    if searchable_columns:
        combined = records[searchable_columns].fillna("").astype(str).agg(" ".join, axis=1)
        display_records = records[combined.str.lower().str.contains(search_query, regex=False)].copy()
    else:
        display_records = records.iloc[0:0].copy()

    section_title = "검색 결과"
    section_copy = "전체 준비 명단에서 검색했습니다."
else:
    display_records = today_records.copy()
    section_title = "오늘 방문"
    section_copy = "방문 시간순으로 표시됩니다."

time_column = columns.get("time")
if time_column and time_column in display_records.columns:
    display_records = display_records.sort_values(
        by=time_column,
        key=lambda series: series.fillna("99:99").astype(str),
        ascending=True,
    )

st.markdown(
    f"""
    <div class="owm-section-head">
        <div>
            <div class="owm-section-title">{section_title}</div>
            <div class="owm-section-copy">{section_copy}</div>
        </div>
        <div class="owm-count">{len(display_records)}명</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if display_records.empty:
    if search_query:
        empty_title = "준비된 명단에서 찾을 수 없습니다."
        empty_copy = "카톡 공지 또는 관리자에게 확인해주세요."
    else:
        empty_title = "오늘 예정된 방문이 없습니다."
        empty_copy = "다른 날짜의 방문자는 위 검색창에서 찾을 수 있습니다."

    st.markdown(
        f"""
        <div class="owm-empty">
            <div class="owm-empty-mark">⌕</div>
            <strong>{empty_title}</strong>
            <span>{empty_copy}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    for _, row in display_records.iterrows():
        visitor_name = value_of(row, columns, "name") or "이름 미입력"
        account = value_of(row, columns, "account")
        phone = value_of(row, columns, "phone")
        visit_date = value_of(row, columns, "date")
        visit_time = value_of(row, columns, "time")
        country = value_of(row, columns, "country")
        shoot_type = value_of(row, columns, "shoot")
        gift = value_of(row, columns, "gift")
        amount = value_of(row, columns, "amount")
        note = value_of(row, columns, "note")
        staff = value_of(row, columns, "staff")
        responded_at = value_of(row, columns, "responded_at")
        response_note = value_of(row, columns, "response_note")
        gift_received = truthy(value_of(row, columns, "gift_received"))
        responded = truthy(value_of(row, columns, "responded"))
        sheet_row = int(row["_sheet_row"])

        badge_class = "done" if responded else "pending"
        badge_text = "응대 완료" if responded else "응대 대기"

        account_html = (
            f'<a class="owm-account" href="{html.escape(account)}" target="_blank">'
            f'{html.escape(account)}</a>'
            if account.startswith(("http://", "https://"))
            else f'<span class="owm-account">{safe(account, "계정주소 미입력")}</span>'
        )

        with st.container(border=True):
            st.markdown(
                f"""
                <div class="owm-visitor-top">
                    <div>
                        <div class="owm-name">{safe(visitor_name)}</div>
                        {account_html}
                    </div>
                    <span class="owm-badge {badge_class}">{badge_text}</span>
                </div>

                <div class="owm-detail-grid">
                    <div class="owm-detail">
                        <div class="owm-detail-label">방문 일정</div>
                        <div class="owm-detail-value">
                            {safe(visit_date)} · {safe(visit_time, "시간 미정")}
                        </div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">국가</div>
                        <div class="owm-detail-value">{safe(country)}</div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">촬영 유형 · 가이드</div>
                        <div class="owm-detail-value">{safe(shoot_type)}</div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">기프트</div>
                        <div class="owm-detail-value">{safe(gift)}</div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">연락처</div>
                        <div class="owm-detail-value">{safe(phone)}</div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">유료금액</div>
                        <div class="owm-detail-value">{format_money(amount)}</div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">기프트 수령</div>
                        <div class="owm-detail-value">
                            {"완료" if gift_received else "미완료"}
                        </div>
                    </div>
                    <div class="owm-detail">
                        <div class="owm-detail-label">응대직원</div>
                        <div class="owm-detail-value">{safe(staff)}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if note:
                st.markdown(
                    f'<div class="owm-note"><b>비고</b><br>{safe(note)}</div>',
                    unsafe_allow_html=True,
                )

            if responded:
                completion_text = (
                    f"{safe(staff, '직원 미입력')} · {safe(responded_at, '시간 미입력')}"
                )
                if response_note:
                    completion_text += f"<br>{safe(response_note)}"

                st.markdown(
                    f"""
                    <div class="owm-done-strip">
                        <b>응대 완료</b><br>{completion_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                action_col, spacer_col = st.columns([1.25, 3.75])
                with action_col:
                    if st.button(
                        "응대 완료",
                        key=f"complete_{sheet_row}",
                        type="primary",
                        use_container_width=True,
                    ):
                        response_dialog(
                            sheet_row=sheet_row,
                            visitor_name=visitor_name,
                            live_mode=live_mode,
                        )

st.markdown(
    '<div class="owm-footer">OWM INFLUENCER DESK · STAFF USE ONLY</div>',
    unsafe_allow_html=True,
)
