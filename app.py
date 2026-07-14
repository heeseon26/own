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
# APP
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OWM Influencer Desk",
    page_icon="◡",
    layout="wide",
    initial_sidebar_state="expanded",
)

KST = ZoneInfo("Asia/Seoul")
LOGO_B64 = "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"

RESPONSE_COLUMNS = ["기프트 수령", "응대 완료", "응대직원", "응대일시", "응대메모"]

ALIASES = {
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
# VISUAL SYSTEM
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        :root {
            --bg: #f4f1ec;
            --panel: #ffffff;
            --ink: #222222;
            --muted: #77716a;
            --line: #e8e2da;
            --dark: #202020;
            --dark-soft: #2a2a29;
            --pink: #d67895;
            --pink-soft: #fff0f4;
            --green: #5f7a65;
            --green-soft: #edf5ef;
            --cream: #faf8f5;
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
            background: var(--bg);
        }

        [data-testid="stAppViewBlockContainer"] {
            padding-top: 2rem;
            padding-bottom: 4.5rem;
            max-width: 1260px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            min-width: 258px;
            max-width: 258px;
            background:
                radial-gradient(circle at 15% 0%, rgba(255,255,255,.06), transparent 16rem),
                linear-gradient(180deg, #242423 0%, #191919 100%);
            border-right: 0;
        }

        [data-testid="stSidebarContent"] {
            padding: 1.55rem 1rem 1rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #d1d1ce;
        }

        .side-brand {
            padding: .3rem .55rem 1.35rem;
            border-bottom: 1px solid rgba(255,255,255,.09);
        }

        .side-brand-row {
            display: flex;
            align-items: center;
            gap: .8rem;
        }

        .side-logo {
            width: 66px;
            height: 49px;
            object-fit: contain;
        }

        .side-title {
            color: #fff;
            font-size: .98rem;
            font-weight: 800;
            letter-spacing: -.015em;
        }

        .side-sub {
            margin-top: .25rem;
            color: #a9a9a5;
            font-size: .69rem;
            letter-spacing: .05em;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: .4rem;
            margin-top: 1.15rem;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label {
            min-height: 3rem;
            padding: .72rem .85rem;
            border: 1px solid transparent;
            border-radius: 14px;
            color: #d2d2cf;
            transition: .16s ease;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255,255,255,.055);
            color: #fff;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: #fff;
            color: #222;
            box-shadow: 0 10px 24px rgba(0,0,0,.22);
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] p {
            color: inherit !important;
            font-size: .86rem;
            font-weight: 760;
        }

        .side-note {
            margin-top: 1.35rem;
            padding: 1rem;
            border: 1px solid rgba(255,255,255,.09);
            border-radius: 16px;
            background: rgba(255,255,255,.045);
            color: #bdbdb9;
            font-size: .71rem;
            line-height: 1.65;
        }

        .side-note b {
            display: block;
            margin-bottom: .3rem;
            color: #f3f3f0;
            font-size: .74rem;
        }

        /* Header */
        .page-kicker {
            color: #9a9188;
            font-size: .7rem;
            font-weight: 760;
            letter-spacing: .13em;
            text-transform: uppercase;
        }

        .page-title {
            margin: .42rem 0 .35rem;
            color: var(--ink);
            font-size: clamp(2rem, 4vw, 3.45rem);
            line-height: 1.03;
            letter-spacing: -.055em;
            font-weight: 850;
        }

        .page-copy {
            max-width: 690px;
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.65;
        }

        .connection-badge {
            display: inline-flex;
            align-items: center;
            gap: .48rem;
            margin-top: 1.1rem;
            padding: .52rem .72rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: rgba(255,255,255,.7);
            color: #77716a;
            font-size: .68rem;
            font-weight: 760;
        }

        .connection-dot {
            width: .45rem;
            height: .45rem;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 0 4px rgba(95,122,101,.12);
        }

        /* Dashboard summary */
        .summary-shell {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 1rem;
            margin: 1.65rem 0 1rem;
        }

        .summary-main {
            min-height: 210px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 1.65rem 1.75rem;
            border-radius: 25px;
            background:
                radial-gradient(circle at 88% 10%, rgba(214,120,149,.18), transparent 17rem),
                linear-gradient(145deg, #292928, #1f1f1f);
            color: #fff;
            box-shadow: 0 22px 52px rgba(34,31,28,.12);
        }

        .summary-date {
            color: #bfbdb8;
            font-size: .72rem;
            font-weight: 720;
            letter-spacing: .08em;
        }

        .summary-main h2 {
            max-width: 540px;
            margin: .72rem 0 0;
            color: #fff;
            font-size: clamp(1.65rem, 3vw, 2.55rem);
            line-height: 1.08;
            letter-spacing: -.045em;
            font-weight: 820;
        }

        .summary-progress {
            margin-top: 1.3rem;
        }

        .summary-progress-line {
            height: 5px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(255,255,255,.11);
        }

        .summary-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: #efb6c6;
        }

        .summary-progress-copy {
            display: flex;
            justify-content: space-between;
            margin-top: .62rem;
            color: #c9c6c0;
            font-size: .69rem;
        }

        .summary-side {
            display: grid;
            grid-template-rows: repeat(2, 1fr);
            gap: 1rem;
        }

        .summary-mini {
            padding: 1.25rem 1.35rem;
            border: 1px solid var(--line);
            border-radius: 22px;
            background: rgba(255,255,255,.86);
        }

        .summary-mini-label {
            color: var(--muted);
            font-size: .73rem;
            font-weight: 720;
        }

        .summary-mini-value {
            margin-top: .4rem;
            color: var(--ink);
            font-size: 2rem;
            line-height: 1;
            font-weight: 850;
            letter-spacing: -.045em;
        }

        .summary-mini-copy {
            margin-top: .45rem;
            color: #9b948d;
            font-size: .68rem;
        }

        /* Section */
        .section-head {
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 1rem;
            margin: 2rem 0 .85rem;
        }

        .section-title {
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 840;
            letter-spacing: -.025em;
        }

        .section-copy {
            margin-top: .28rem;
            color: var(--muted);
            font-size: .78rem;
        }

        .section-count {
            color: #9a938b;
            font-size: .7rem;
            font-weight: 720;
        }

        /* Search */
        div[data-testid="stTextInput"] input {
            min-height: 3.35rem;
            padding: 0 1.05rem;
            border: 1px solid var(--line);
            border-radius: 17px;
            background: rgba(255,255,255,.93);
            color: var(--ink);
            font-size: .94rem;
            box-shadow: none;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: rgba(214,120,149,.72);
            box-shadow: 0 0 0 4px rgba(214,120,149,.1);
        }

        /* Visitor cards */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--line) !important;
            border-radius: 22px !important;
            background: rgba(255,255,255,.94) !important;
            box-shadow: 0 10px 28px rgba(36,31,27,.035) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #dcd4ca !important;
        }

        .visitor-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .visitor-id {
            display: flex;
            align-items: center;
            gap: .8rem;
            min-width: 0;
        }

        .visitor-avatar {
            width: 44px;
            height: 44px;
            flex: 0 0 auto;
            display: grid;
            place-items: center;
            border-radius: 14px;
            background: var(--pink-soft);
            color: #a75b74;
            font-size: .78rem;
            font-weight: 850;
        }

        .visitor-name {
            color: var(--ink);
            font-size: 1.02rem;
            font-weight: 830;
            letter-spacing: -.02em;
        }

        .visitor-account {
            display: block;
            max-width: 690px;
            margin-top: .25rem;
            overflow: hidden;
            color: var(--muted);
            font-size: .74rem;
            text-decoration: none;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            padding: .42rem .66rem;
            border-radius: 999px;
            font-size: .68rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .status-pill.pending {
            color: #94566e;
            background: var(--pink-soft);
        }

        .status-pill.done {
            color: #4f6d56;
            background: var(--green-soft);
        }

        .detail-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: .65rem;
        }

        .detail {
            min-width: 0;
            padding: .78rem .85rem;
            border-radius: 14px;
            background: var(--cream);
        }

        .detail-label {
            margin-bottom: .32rem;
            color: #968f87;
            font-size: .64rem;
            font-weight: 730;
        }

        .detail-value {
            overflow: hidden;
            color: #3f3a36;
            font-size: .78rem;
            font-weight: 700;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .note-box {
            margin-top: .7rem;
            padding: .82rem .9rem;
            border-left: 3px solid #e6a8bb;
            border-radius: 4px 13px 13px 4px;
            background: #fff7f9;
            color: #714b58;
            font-size: .75rem;
            line-height: 1.58;
        }

        .complete-strip {
            margin-top: .72rem;
            padding: .78rem .9rem;
            border-radius: 13px;
            background: #f2f7f3;
            color: #55705c;
            font-size: .74rem;
            line-height: 1.55;
        }

        .complete-strip b {
            color: #47604d;
        }

        /* Buttons and forms */
        div.stButton > button {
            min-height: 2.78rem;
            border: 1px solid var(--line);
            border-radius: 13px;
            background: #fff;
            color: #333;
            font-weight: 790;
            transition: .14s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-1px);
            border-color: #d8cfc5;
            box-shadow: 0 8px 18px rgba(36,31,27,.07);
        }

        div.stButton > button[kind="primary"] {
            border-color: var(--dark);
            background: var(--dark);
            color: white;
        }

        div[data-testid="stCheckbox"] label p,
        div[data-testid="stTextArea"] label p,
        div[data-testid="stTextInput"] label p {
            color: #5d5751;
            font-size: .76rem;
            font-weight: 740;
        }

        div[data-testid="stTextArea"] textarea {
            border: 1px solid var(--line);
            border-radius: 13px;
        }

        div[role="dialog"] {
            border-radius: 22px !important;
        }

        /* Empty state */
        .empty {
            padding: 3rem 1.35rem;
            border: 1px dashed #d7cec4;
            border-radius: 22px;
            background: rgba(255,255,255,.56);
            color: var(--muted);
            text-align: center;
        }

        .empty-mark {
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            margin: 0 auto .78rem;
            border-radius: 13px;
            background: var(--pink-soft);
            color: var(--pink);
            font-size: 1rem;
            font-weight: 850;
        }

        .empty strong {
            display: block;
            margin-bottom: .3rem;
            color: var(--ink);
            font-size: .9rem;
        }

        /* History */
        .history-row {
            display: grid;
            grid-template-columns: minmax(170px, 1.2fr) 1fr 1fr 1.3fr;
            gap: .9rem;
            align-items: center;
            padding: 1rem 1.05rem;
            border-bottom: 1px solid var(--line);
        }

        .history-row:last-child {
            border-bottom: 0;
        }

        .history-name {
            color: var(--ink);
            font-size: .83rem;
            font-weight: 800;
        }

        .history-sub,
        .history-cell {
            color: var(--muted);
            font-size: .72rem;
        }

        .history-sub {
            margin-top: .22rem;
        }

        .history-wrap {
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(255,255,255,.9);
        }

        .footer-note {
            margin-top: 2.5rem;
            color: #a39b93;
            font-size: .66rem;
            text-align: center;
            letter-spacing: .04em;
        }

        @media (max-width: 980px) {
            .summary-shell {
                grid-template-columns: 1fr;
            }

            .summary-side {
                grid-template-columns: repeat(2, minmax(0,1fr));
                grid-template-rows: none;
            }

            .detail-grid {
                grid-template-columns: repeat(2, minmax(0,1fr));
            }
        }

        @media (max-width: 650px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .summary-side {
                grid-template-columns: 1fr;
            }

            .detail-grid {
                grid-template-columns: 1fr;
            }

            .visitor-head {
                flex-direction: column;
            }

            .history-row {
                grid-template-columns: 1fr;
                gap: .35rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# GOOGLE SHEETS
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
def worksheet():
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

    spreadsheet_id = st.secrets["sheet"]["spreadsheet_id"]
    worksheet_name = st.secrets["sheet"].get("worksheet_name", "인플루언서")
    return client.open_by_key(spreadsheet_id).worksheet(worksheet_name)


def ensure_response_columns(ws) -> list[str]:
    headers = [str(value).strip() for value in ws.row_values(1)]
    missing = [column for column in RESPONSE_COLUMNS if column not in headers]
    if missing:
        headers.extend(missing)
        ws.update(range_name="A1", values=[headers])
    return headers


@st.cache_data(ttl=15, show_spinner=False)
def load_sheet() -> pd.DataFrame:
    ws = worksheet()
    if ws is None:
        return pd.DataFrame()

    headers = ensure_response_columns(ws)
    values = ws.get_all_values()

    if len(values) <= 1:
        return pd.DataFrame(columns=headers + ["_sheet_row"])

    rows = []
    for raw in values[1:]:
        row = raw + [""] * max(0, len(headers) - len(raw))
        rows.append(row[: len(headers)])

    frame = pd.DataFrame(rows, columns=headers)
    frame["_sheet_row"] = range(2, len(frame) + 2)
    return frame


def preview_data() -> pd.DataFrame:
    today = datetime.now(KST).strftime("%Y-%m-%d")
    return pd.DataFrame(
        [
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
                "비고": "Google Sheets 연결 전 화면 확인용 예시입니다.",
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
    )


def records() -> tuple[pd.DataFrame, bool, str]:
    if has_sheet_config():
        try:
            return load_sheet(), True, ""
        except Exception as exc:
            return pd.DataFrame(), False, str(exc)

    if "preview_records" not in st.session_state:
        st.session_state.preview_records = preview_data()
    return st.session_state.preview_records.copy(), False, ""


def resolve_columns(columns: list[str]) -> dict[str, str | None]:
    normalized = {str(column).strip(): str(column) for column in columns}
    result: dict[str, str | None] = {}
    for key, aliases in ALIASES.items():
        result[key] = next(
            (normalized[alias] for alias in aliases if alias in normalized),
            None,
        )
    return result


def cell(row: pd.Series, resolved: dict[str, str | None], key: str) -> str:
    column = resolved.get(key)
    if not column:
        return ""
    value = row.get(column, "")
    if pd.isna(value):
        return ""
    return str(value).strip()


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {
        "true", "1", "yes", "y", "o", "예", "완료", "⭕", "checked"
    }


def normalize_date(value: str) -> str:
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


def safe(value: Any, fallback: str = "-") -> str:
    text = "" if value is None else str(value).strip()
    return html.escape(text or fallback)


def initials(name: str) -> str:
    cleaned = str(name).strip()
    return html.escape(cleaned[:2] if cleaned else "OW")


def money(value: str) -> str:
    text = str(value).strip().replace(",", "").replace("₩", "").replace("원", "")
    if not text:
        return "-"
    try:
        return f"₩{int(float(text)):,}"
    except ValueError:
        return safe(value)


def save_response(
    sheet_row: int,
    staff_name: str,
    gift_received: bool,
    response_note: str,
    live_mode: bool,
) -> None:
    timestamp = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    updates = {
        "기프트 수령": "TRUE" if gift_received else "FALSE",
        "응대 완료": "TRUE",
        "응대직원": staff_name.strip(),
        "응대일시": timestamp,
        "응대메모": response_note.strip(),
    }

    if live_mode:
        ws = worksheet()
        if ws is None:
            raise RuntimeError("Google Sheets가 연결되지 않았습니다.")

        headers = ensure_response_columns(ws)
        cells = []
        for header, value in updates.items():
            column_index = headers.index(header) + 1
            cells.append(gspread.Cell(int(sheet_row), column_index, value))
        ws.update_cells(cells, value_input_option="USER_ENTERED")
        load_sheet.clear()
        return

    frame = st.session_state.preview_records.copy()
    mask = frame["_sheet_row"].astype(int) == int(sheet_row)
    for header, value in updates.items():
        frame.loc[mask, header] = value
    st.session_state.preview_records = frame


# ─────────────────────────────────────────────────────────────
# DIALOG
# ─────────────────────────────────────────────────────────────
@st.dialog("응대 완료", width="small")
def complete_dialog(
    sheet_row: int,
    visitor_name: str,
    live_mode: bool,
) -> None:
    st.markdown(f"**{html.escape(visitor_name)}** 님의 응대 기록을 남깁니다.")

    with st.form(f"complete_form_{sheet_row}"):
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
            save_response(
                sheet_row=sheet_row,
                staff_name=staff_name,
                gift_received=gift_received,
                response_note=response_note,
                live_mode=live_mode,
            )
            st.toast("응대 완료로 표시했습니다.", icon="✓")
            st.rerun()
        except Exception:
            st.error("저장하지 못했습니다. 관리자에게 확인해주세요.")


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
        <div class="side-brand">
            <div class="side-brand-row">
                <img class="side-logo" src="data:image/png;base64,{LOGO_B64}" alt="OWM">
                <div>
                    <div class="side-title">Influencer Desk</div>
                    <div class="side-sub">OPTIMA WELLNESS · SINSA</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "메뉴",
        ["오늘 방문", "전체 검색", "응대 기록"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="side-note">
            <b>직원 사용 안내</b>
            준비된 명단에서 방문자를 확인한 뒤
            응대를 마치면 해당 손님의 <b>응대 완료</b>만 표시합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# DATA PREP
# ─────────────────────────────────────────────────────────────
frame, live_mode, connection_error = records()
resolved = resolve_columns(list(frame.columns))

today = datetime.now(KST).strftime("%Y-%m-%d")
today_label = datetime.now(KST).strftime("%Y년 %m월 %d일")

if not frame.empty and resolved.get("date"):
    today_mask = frame[resolved["date"]].map(normalize_date) == today
else:
    today_mask = pd.Series(False, index=frame.index)

if not frame.empty and resolved.get("responded"):
    done_mask = frame[resolved["responded"]].map(truthy)
else:
    done_mask = pd.Series(False, index=frame.index)

today_frame = frame[today_mask].copy() if not frame.empty else frame.copy()
today_total = int(today_mask.sum()) if len(today_mask) else 0
today_done = int((today_mask & done_mask).sum()) if len(today_mask) else 0
today_pending = max(today_total - today_done, 0)
progress = int(round((today_done / today_total) * 100)) if today_total else 0

connection_text = "GOOGLE SHEET CONNECTED" if live_mode else "PREVIEW MODE"


def page_header(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="page-kicker">{html.escape(kicker)}</div>
        <div class="page-title">{title}</div>
        <div class="page-copy">{html.escape(copy)}</div>
        <div class="connection-badge">
            <span class="connection-dot"></span>
            {connection_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def visitor_card(row: pd.Series) -> None:
    name = cell(row, resolved, "name") or "이름 미입력"
    account = cell(row, resolved, "account")
    phone = cell(row, resolved, "phone")
    visit_date = cell(row, resolved, "date")
    visit_time = cell(row, resolved, "time")
    country = cell(row, resolved, "country")
    shoot = cell(row, resolved, "shoot")
    gift = cell(row, resolved, "gift")
    amount = cell(row, resolved, "amount")
    note = cell(row, resolved, "note")
    staff = cell(row, resolved, "staff")
    responded_at = cell(row, resolved, "responded_at")
    response_note = cell(row, resolved, "response_note")
    gift_received = truthy(cell(row, resolved, "gift_received"))
    responded = truthy(cell(row, resolved, "responded"))
    sheet_row = int(row["_sheet_row"])

    status_class = "done" if responded else "pending"
    status_text = "응대 완료" if responded else "응대 대기"

    if account.startswith(("http://", "https://")):
        account_html = (
            f'<a class="visitor-account" href="{html.escape(account)}" target="_blank">'
            f'{html.escape(account)}</a>'
        )
    else:
        account_html = f'<span class="visitor-account">{safe(account, "계정주소 미입력")}</span>'

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="visitor-head">
                <div class="visitor-id">
                    <div class="visitor-avatar">{initials(name)}</div>
                    <div style="min-width:0">
                        <div class="visitor-name">{safe(name)}</div>
                        {account_html}
                    </div>
                </div>
                <span class="status-pill {status_class}">{status_text}</span>
            </div>

            <div class="detail-grid">
                <div class="detail">
                    <div class="detail-label">방문 일정</div>
                    <div class="detail-value">{safe(visit_date)} · {safe(visit_time, "시간 미정")}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">국가</div>
                    <div class="detail-value">{safe(country)}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">촬영 유형 · 가이드</div>
                    <div class="detail-value">{safe(shoot)}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">기프트</div>
                    <div class="detail-value">{safe(gift)}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">연락처</div>
                    <div class="detail-value">{safe(phone)}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">유료금액</div>
                    <div class="detail-value">{money(amount)}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">기프트 수령</div>
                    <div class="detail-value">{"완료" if gift_received else "미완료"}</div>
                </div>
                <div class="detail">
                    <div class="detail-label">응대직원</div>
                    <div class="detail-value">{safe(staff)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if note:
            st.markdown(
                f'<div class="note-box"><b>비고</b><br>{safe(note)}</div>',
                unsafe_allow_html=True,
            )

        if responded:
            completion = f"{safe(staff, '직원 미입력')} · {safe(responded_at, '시간 미입력')}"
            if response_note:
                completion += f"<br>{safe(response_note)}"

            st.markdown(
                f"""
                <div class="complete-strip">
                    <b>응대 완료</b><br>{completion}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            action, _ = st.columns([1.1, 3.9])
            with action:
                if st.button(
                    "응대 완료",
                    key=f"complete_{sheet_row}_{page}",
                    type="primary",
                    use_container_width=True,
                ):
                    complete_dialog(
                        sheet_row=sheet_row,
                        visitor_name=name,
                        live_mode=live_mode,
                    )


def sort_by_time(data: pd.DataFrame) -> pd.DataFrame:
    time_col = resolved.get("time")
    if time_col and time_col in data.columns:
        return data.sort_values(
            by=time_col,
            key=lambda series: series.fillna("99:99").astype(str),
        )
    return data


def empty_state(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="empty">
            <div class="empty-mark">⌕</div>
            <strong>{html.escape(title)}</strong>
            <span>{html.escape(copy)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


if connection_error:
    st.error("Google Sheets 연결에 실패했습니다. 관리자에게 확인해주세요.")


# ─────────────────────────────────────────────────────────────
# PAGE: TODAY
# ─────────────────────────────────────────────────────────────
if page == "오늘 방문":
    page_header(
        "TODAY",
        "오늘의 방문을<br>한눈에 확인하세요.",
        "미리 준비된 명단을 확인하고, 응대를 마친 직원은 완료 표시만 남기면 됩니다.",
    )

    st.markdown(
        f"""
        <div class="summary-shell">
            <div class="summary-main">
                <div>
                    <div class="summary-date">{today_label}</div>
                    <h2>오늘 {today_total}명의 방문이 예정되어 있습니다.</h2>
                </div>
                <div class="summary-progress">
                    <div class="summary-progress-line">
                        <div class="summary-progress-fill" style="width:{progress}%"></div>
                    </div>
                    <div class="summary-progress-copy">
                        <span>응대 진행률</span>
                        <span>{progress}%</span>
                    </div>
                </div>
            </div>
            <div class="summary-side">
                <div class="summary-mini">
                    <div class="summary-mini-label">응대 완료</div>
                    <div class="summary-mini-value">{today_done}</div>
                    <div class="summary-mini-copy">오늘 처리된 방문</div>
                </div>
                <div class="summary-mini">
                    <div class="summary-mini-label">응대 대기</div>
                    <div class="summary-mini-value">{today_pending}</div>
                    <div class="summary-mini-copy">아직 확인이 필요한 방문</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "오늘 방문 검색",
        placeholder="오늘 방문자 이름 · 계정 · 연락처 검색",
        label_visibility="collapsed",
    ).strip().lower()

    display = today_frame.copy()
    if query:
        search_cols = [
            resolved.get("name"),
            resolved.get("account"),
            resolved.get("phone"),
            resolved.get("country"),
        ]
        search_cols = [column for column in search_cols if column]
        if search_cols:
            combined = display[search_cols].fillna("").astype(str).agg(" ".join, axis=1)
            display = display[combined.str.lower().str.contains(query, regex=False)]

    display = sort_by_time(display)

    st.markdown(
        f"""
        <div class="section-head">
            <div>
                <div class="section-title">오늘 방문 일정</div>
                <div class="section-copy">방문 시간순으로 표시됩니다.</div>
            </div>
            <div class="section-count">{len(display)}명</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if display.empty:
        empty_state(
            "오늘 표시할 방문자가 없습니다.",
            "다른 날짜의 방문자는 전체 검색에서 확인할 수 있습니다.",
        )
    else:
        for _, row in display.iterrows():
            visitor_card(row)


# ─────────────────────────────────────────────────────────────
# PAGE: SEARCH
# ─────────────────────────────────────────────────────────────
elif page == "전체 검색":
    page_header(
        "SEARCH",
        "필요한 방문자를<br>바로 찾아보세요.",
        "이름, 계정 주소, 연락처 가운데 일부만 입력해도 준비된 전체 명단에서 검색됩니다.",
    )

    query = st.text_input(
        "전체 명단 검색",
        placeholder="이름 · 인스타 계정 · 연락처 검색",
        label_visibility="collapsed",
    ).strip().lower()

    if not query:
        st.markdown(
            """
            <div class="section-head">
                <div>
                    <div class="section-title">전체 명단 검색</div>
                    <div class="section-copy">검색어를 입력하면 해당 방문 정보만 표시됩니다.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        empty_state(
            "검색어를 입력해주세요.",
            "준비된 명단에 없는 방문자는 관리자에게 확인해주세요.",
        )
    else:
        search_cols = [
            resolved.get("name"),
            resolved.get("account"),
            resolved.get("phone"),
            resolved.get("country"),
            resolved.get("shoot"),
        ]
        search_cols = [column for column in search_cols if column]

        if search_cols:
            combined = frame[search_cols].fillna("").astype(str).agg(" ".join, axis=1)
            display = frame[combined.str.lower().str.contains(query, regex=False)].copy()
        else:
            display = frame.iloc[0:0].copy()

        date_col = resolved.get("date")
        if date_col and date_col in display.columns:
            display["_sort_date"] = display[date_col].map(normalize_date)
            display = display.sort_values("_sort_date", ascending=False)

        st.markdown(
            f"""
            <div class="section-head">
                <div>
                    <div class="section-title">검색 결과</div>
                    <div class="section-copy">전체 준비 명단에서 조회했습니다.</div>
                </div>
                <div class="section-count">{len(display)}명</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if display.empty:
            empty_state(
                "준비된 명단에서 찾을 수 없습니다.",
                "카톡 공지 또는 관리자에게 확인해주세요.",
            )
        else:
            for _, row in display.iterrows():
                visitor_card(row)


# ─────────────────────────────────────────────────────────────
# PAGE: HISTORY
# ─────────────────────────────────────────────────────────────
else:
    page_header(
        "HISTORY",
        "완료된 응대 기록을<br>차분하게 확인하세요.",
        "누가 어떤 방문자를 응대했는지 확인하는 읽기 전용 기록입니다.",
    )

    completed = frame[done_mask].copy() if not frame.empty else frame.copy()
    search_history = st.text_input(
        "응대 기록 검색",
        placeholder="방문자명 · 응대직원 검색",
        label_visibility="collapsed",
    ).strip().lower()

    if search_history and not completed.empty:
        history_cols = [resolved.get("name"), resolved.get("staff"), resolved.get("account")]
        history_cols = [column for column in history_cols if column]
        if history_cols:
            combined = completed[history_cols].fillna("").astype(str).agg(" ".join, axis=1)
            completed = completed[
                combined.str.lower().str.contains(search_history, regex=False)
            ]

    responded_at_col = resolved.get("responded_at")
    if responded_at_col and responded_at_col in completed.columns:
        completed = completed.sort_values(responded_at_col, ascending=False)

    st.markdown(
        f"""
        <div class="section-head">
            <div>
                <div class="section-title">응대 완료 기록</div>
                <div class="section-copy">최근 기록부터 표시됩니다.</div>
            </div>
            <div class="section-count">{len(completed)}건</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if completed.empty:
        empty_state(
            "아직 응대 완료 기록이 없습니다.",
            "방문 확인 화면에서 응대 완료를 저장하면 여기에 표시됩니다.",
        )
    else:
        rows_html = []
        for _, row in completed.iterrows():
            name = cell(row, resolved, "name") or "이름 미입력"
            account = cell(row, resolved, "account")
            staff = cell(row, resolved, "staff")
            responded_at = cell(row, resolved, "responded_at")
            gift_received = truthy(cell(row, resolved, "gift_received"))
            response_note = cell(row, resolved, "response_note")

            rows_html.append(
                f"""
                <div class="history-row">
                    <div>
                        <div class="history-name">{safe(name)}</div>
                        <div class="history-sub">{safe(account, "계정주소 미입력")}</div>
                    </div>
                    <div class="history-cell">응대직원<br><b>{safe(staff)}</b></div>
                    <div class="history-cell">기프트 수령<br><b>{"완료" if gift_received else "미완료"}</b></div>
                    <div class="history-cell">
                        {safe(responded_at, "시간 미입력")}
                        {"<br>" + safe(response_note) if response_note else ""}
                    </div>
                </div>
                """
            )

        st.markdown(
            '<div class="history-wrap">' + "".join(rows_html) + "</div>",
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="footer-note">OWM INFLUENCER DESK · STAFF USE ONLY</div>',
    unsafe_allow_html=True,
)
