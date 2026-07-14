from __future__ import annotations

import base64
import hashlib
import io
import re
import shutil
import uuid
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:  # 로컬에서 requirements 설치 전에도 파일을 열어볼 수 있도록 처리
    gspread = None
    Credentials = None


# ──────────────────────────────────────────────────────────────────────────────
# 기본 설정
# ──────────────────────────────────────────────────────────────────────────────
APP_TITLE = "OWM Influencer Desk"
APP_SUBTITLE = "옵티마웰니스 신사점 인플루언서 통합 관리"
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "owm_logo_transparent.png"
LOCAL_DATA_PATH = BASE_DIR / "data" / "local_data.csv"
SAMPLE_DATA_PATH = BASE_DIR / "sample_data.csv"

COLUMNS = [
    "record_id",
    "협찬일",
    "방문 시간",
    "국가",
    "계정주소",
    "방문자명",
    "연락처",
    "촬영 유형/가이드",
    "기프트",
    "유료금액",
    "비고",
    "기프트 수령",
    "응대직원",
    "진행상태",
    "등록경로",
    "등록일시",
    "최종수정일시",
]

VISIBLE_COLUMNS = [
    "협찬일",
    "방문 시간",
    "국가",
    "방문자명",
    "계정주소",
    "연락처",
    "촬영 유형/가이드",
    "기프트",
    "유료금액",
    "진행상태",
    "기프트 수령",
    "응대직원",
    "비고",
]

STATUS_OPTIONS = ["방문 예정", "촬영 진행", "촬영 완료", "취소"]
SOURCE_OPTIONS = ["기존 명단", "카톡 공지", "현장 신규", "CSV 가져오기", "기타"]
COUNTRY_OPTIONS = ["영어권", "중국", "일본", "대만", "홍콩", "러시아", "기타 국가", "미입력"]

COLUMN_ALIASES = {
    "협찬일": "협찬일",
    "날짜": "협찬일",
    "방문일": "협찬일",
    "방문시간": "방문 시간",
    "방문 시간": "방문 시간",
    "국가": "국가",
    "계정주소": "계정주소",
    "계정 주소": "계정주소",
    "인스타": "계정주소",
    "인스타그램": "계정주소",
    "방문자명": "방문자명",
    "방문자 명": "방문자명",
    "이름": "방문자명",
    "연락처": "연락처",
    "촬영유형선택/가이드": "촬영 유형/가이드",
    "촬영 유형 선택/가이드": "촬영 유형/가이드",
    "촬영유형/가이드": "촬영 유형/가이드",
    "촬영 유형/가이드": "촬영 유형/가이드",
    "촬영유형": "촬영 유형/가이드",
    "가이드": "촬영 유형/가이드",
    "기프트": "기프트",
    "gift": "기프트",
    "유료금액": "유료금액",
    "유료 금액": "유료금액",
    "금액": "유료금액",
    "비고": "비고",
    "메모": "비고",
    "기프트수령": "기프트 수령",
    "기프트 수령": "기프트 수령",
    "응대직원": "응대직원",
    "응대 직원": "응대직원",
    "진행상태": "진행상태",
    "진행 상태": "진행상태",
    "등록경로": "등록경로",
    "등록 경로": "등록경로",
}

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────────────────────────────────────
# 스타일
# ──────────────────────────────────────────────────────────────────────────────
def get_logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        return ""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --owm-dark: #232323;
            --owm-ink: #282522;
            --owm-muted: #77716b;
            --owm-pink: #d987a3;
            --owm-pink-soft: #fff0f5;
            --owm-cream: #f6f1eb;
            --owm-line: #ebe3dc;
        }
        .stApp { background: var(--owm-cream); }
        [data-testid="stSidebar"] { background: #222222; }
        [data-testid="stSidebar"] * { color: #f7f7f7; }
        [data-testid="stSidebar"] .stAlert * { color: #282522; }
        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.15); }
        .block-container { padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1500px; }
        .owm-hero {
            background: linear-gradient(135deg, #232323 0%, #32302f 70%, #4a3a40 100%);
            border-radius: 26px;
            padding: 22px 28px;
            color: white;
            display: flex;
            align-items: center;
            gap: 20px;
            box-shadow: 0 16px 45px rgba(44, 36, 34, .14);
            margin-bottom: 18px;
        }
        .owm-hero img { width: 105px; height: 76px; object-fit: contain; }
        .owm-hero h1 { margin: 0; font-size: 2rem; letter-spacing: -.04em; }
        .owm-hero p { margin: 7px 0 0; color: #ded8d5; font-size: .95rem; }
        .owm-card {
            background: rgba(255,255,255,.93);
            border: 1px solid var(--owm-line);
            border-radius: 20px;
            padding: 18px 20px;
            box-shadow: 0 10px 32px rgba(50, 39, 34, .06);
            margin-bottom: 14px;
        }
        .owm-card h3 { margin: 0 0 7px; font-size: 1.05rem; }
        .owm-card p { margin: 0; color: var(--owm-muted); }
        .owm-pill {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: var(--owm-pink-soft);
            color: #a74e70;
            font-size: .78rem;
            font-weight: 750;
            margin: 2px 5px 2px 0;
        }
        .owm-muted { color: var(--owm-muted); font-size: .9rem; }
        .owm-result-title { font-size: 1.25rem; font-weight: 800; margin-bottom: 3px; }
        .owm-link { color: #a74e70 !important; text-decoration: none; font-weight: 700; }
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid var(--owm-line);
            padding: 14px 16px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(50, 39, 34, .05);
        }
        div[data-testid="stMetricLabel"] { color: var(--owm-muted); }
        .stButton > button, .stDownloadButton > button {
            border-radius: 12px;
            font-weight: 750;
            min-height: 42px;
        }
        .stButton > button[kind="primary"] {
            background: #282522;
            border-color: #282522;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input, .stDateInput input, .stTimeInput input {
            border-radius: 12px !important;
        }
        div[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; }
        [data-testid="stTabs"] button { font-weight: 750; }
        @media (max-width: 800px) {
            .owm-hero { padding: 18px; }
            .owm-hero img { width: 70px; height: 52px; }
            .owm-hero h1 { font-size: 1.45rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# ──────────────────────────────────────────────────────────────────────────────
# 공통 유틸리티
# ──────────────────────────────────────────────────────────────────────────────
def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return clean_text(value).lower() in {"true", "1", "yes", "y", "완료", "수령", "o", "⭕", "체크"}


def normalize_date(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return text
    return parsed.strftime("%Y-%m-%d")


def normalize_time(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return text
    return parsed.strftime("%H:%M")


def normalize_money(value: Any) -> int:
    text = re.sub(r"[^0-9.-]", "", clean_text(value))
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


def format_money(value: Any) -> str:
    amount = normalize_money(value)
    return f"₩{amount:,}" if amount else "-"


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    for column in COLUMNS:
        if column not in output.columns:
            output[column] = ""
    output = output[COLUMNS]
    output = output.fillna("")
    output["협찬일"] = output["협찬일"].map(normalize_date)
    output["방문 시간"] = output["방문 시간"].map(normalize_time)
    output["기프트 수령"] = output["기프트 수령"].map(to_bool)
    output["유료금액"] = output["유료금액"].map(normalize_money)
    output["진행상태"] = output["진행상태"].map(lambda x: clean_text(x) or "방문 예정")
    return output


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def account_href(account: str) -> str:
    account = clean_text(account)
    if not account:
        return ""
    if account.startswith(("http://", "https://")):
        return account
    if account.startswith("@"):
        return f"https://www.instagram.com/{account[1:]}/"
    return ""


def make_record_id() -> str:
    return uuid.uuid4().hex[:12]


def ensure_unique_record_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    seen: set[str] = set()
    for idx in df.index:
        rid = clean_text(df.at[idx, "record_id"])
        if not rid or rid in seen:
            rid = make_record_id()
            df.at[idx, "record_id"] = rid
        seen.add(rid)
    return df


def dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=VISIBLE_COLUMNS)
    display = df[VISIBLE_COLUMNS].copy()
    display["유료금액"] = display["유료금액"].map(format_money)
    display["기프트 수령"] = display["기프트 수령"].map(lambda x: "⭕" if to_bool(x) else "")
    return display


def normalize_header(text: Any) -> str:
    value = re.sub(r"\s+", " ", clean_text(text)).strip()
    compact = value.replace(" ", "")
    return COLUMN_ALIASES.get(value, COLUMN_ALIASES.get(compact, value))


def import_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    renamed = raw_df.copy()
    renamed.columns = [normalize_header(column) for column in renamed.columns]
    # 중복 열이 생기면 첫 번째 비어 있지 않은 값을 사용
    if renamed.columns.duplicated().any():
        merged: dict[str, pd.Series] = {}
        for column in dict.fromkeys(renamed.columns):
            same = renamed.loc[:, renamed.columns == column]
            merged[column] = same.replace("", pd.NA).bfill(axis=1).iloc[:, 0].fillna("")
        renamed = pd.DataFrame(merged)

    now = now_text()
    result = pd.DataFrame(index=renamed.index)
    for column in COLUMNS:
        result[column] = renamed[column] if column in renamed.columns else ""
    result["record_id"] = result["record_id"].map(clean_text)
    result["record_id"] = result["record_id"].map(lambda x: x or make_record_id())
    result["등록경로"] = result["등록경로"].map(lambda x: clean_text(x) or "CSV 가져오기")
    result["진행상태"] = result["진행상태"].map(lambda x: clean_text(x) or "방문 예정")
    result["등록일시"] = result["등록일시"].map(lambda x: clean_text(x) or now)
    result["최종수정일시"] = result["최종수정일시"].map(lambda x: clean_text(x) or now)
    return ensure_unique_record_ids(normalize_dataframe(result))


def safe_rerun() -> None:
    st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# 저장소: Google Sheets 또는 로컬 CSV
# ──────────────────────────────────────────────────────────────────────────────
class StorageError(RuntimeError):
    pass


@dataclass
class BackendInfo:
    mode: str
    label: str
    detail: str


def secret_value(section: str, key: str, default: Any = None) -> Any:
    try:
        section_data = st.secrets.get(section, {})
        return section_data.get(key, default)
    except Exception:
        return default


def has_google_secrets() -> bool:
    try:
        service_info = st.secrets.get("gcp_service_account", {})
        spreadsheet_id = secret_value("app", "spreadsheet_id", "")
        return bool(service_info and spreadsheet_id)
    except Exception:
        return False


def column_letter(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


@st.cache_resource(show_spinner=False)
def google_worksheet():
    if gspread is None or Credentials is None:
        raise StorageError("Google Sheets 패키지가 설치되지 않았습니다. requirements.txt를 확인하세요.")
    try:
        info = dict(st.secrets["gcp_service_account"])
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(str(st.secrets["app"]["spreadsheet_id"]))
        worksheet_name = secret_value("app", "worksheet_name", "OWM_통합관리")
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=2000,
                cols=max(20, len(COLUMNS)),
            )
        initialize_google_worksheet(worksheet)
        return worksheet
    except Exception as exc:
        raise StorageError(f"Google Sheets 연결 실패: {exc}") from exc


def initialize_google_worksheet(worksheet) -> None:
    values = worksheet.get_all_values()
    headers = [clean_text(item) for item in values[0]] if values else []

    if not headers:
        worksheet.update([COLUMNS], "A1", value_input_option="RAW")
    elif headers != COLUMNS:
        # 기존 형식의 열을 발견하면 앱 표준 열로 안전하게 재정렬합니다.
        rows = values[1:]
        width = len(headers)
        padded_rows = [row[:width] + [""] * max(0, width - len(row)) for row in rows]
        migrated = import_dataframe(pd.DataFrame(padded_rows, columns=headers)) if rows else pd.DataFrame(columns=COLUMNS)
        worksheet.clear()
        matrix = [COLUMNS]
        if not migrated.empty:
            matrix.extend(
                [
                    [serialize_sheet_value(record.get(column, "")) for column in COLUMNS]
                    for record in migrated.to_dict("records")
                ]
            )
        worksheet.update(matrix, "A1", value_input_option="USER_ENTERED")
    try:
        worksheet.freeze(rows=1)
        last = column_letter(len(COLUMNS))
        worksheet.format(
            f"A1:{last}1",
            {
                "backgroundColor": {"red": 0.15, "green": 0.15, "blue": 0.15},
                "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
                "horizontalAlignment": "CENTER",
            },
        )
        worksheet.set_basic_filter(f"A1:{last}")
    except Exception:
        # 서식 적용 권한/쿼터 문제가 있어도 데이터 기능은 계속 사용
        pass


def load_google_data() -> pd.DataFrame:
    worksheet = google_worksheet()
    values = worksheet.get_all_values()
    if not values:
        return pd.DataFrame(columns=COLUMNS)
    header = [clean_text(item) for item in values[0]]
    rows = values[1:]
    if not rows:
        return pd.DataFrame(columns=COLUMNS)
    width = len(header)
    padded_rows = [row[:width] + [""] * max(0, width - len(row)) for row in rows]
    df = pd.DataFrame(padded_rows, columns=header)
    return normalize_dataframe(df)


def find_google_row(record_id: str) -> int:
    worksheet = google_worksheet()
    ids = worksheet.col_values(1)
    for index, value in enumerate(ids[1:], start=2):
        if clean_text(value) == record_id:
            return index
    raise StorageError("수정할 기록을 찾지 못했습니다. 새로고침 후 다시 시도해주세요.")


def add_google_record(record: dict[str, Any]) -> None:
    row = [serialize_sheet_value(record.get(column, "")) for column in COLUMNS]
    google_worksheet().append_row(row, value_input_option="USER_ENTERED")


def add_google_records(records: Iterable[dict[str, Any]]) -> None:
    rows = [[serialize_sheet_value(record.get(column, "")) for column in COLUMNS] for record in records]
    if rows:
        google_worksheet().append_rows(rows, value_input_option="USER_ENTERED")


def update_google_record(record_id: str, record: dict[str, Any]) -> None:
    worksheet = google_worksheet()
    row_index = find_google_row(record_id)
    values = [[serialize_sheet_value(record.get(column, "")) for column in COLUMNS]]
    last = column_letter(len(COLUMNS))
    worksheet.update(values, f"A{row_index}:{last}{row_index}", value_input_option="USER_ENTERED")


def delete_google_record(record_id: str) -> None:
    row_index = find_google_row(record_id)
    google_worksheet().delete_rows(row_index)


def serialize_sheet_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return value


def initialize_local_data() -> None:
    LOCAL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOCAL_DATA_PATH.exists():
        return
    if SAMPLE_DATA_PATH.exists():
        shutil.copy2(SAMPLE_DATA_PATH, LOCAL_DATA_PATH)
    else:
        pd.DataFrame(columns=COLUMNS).to_csv(LOCAL_DATA_PATH, index=False, encoding="utf-8-sig")


def load_local_data() -> pd.DataFrame:
    initialize_local_data()
    try:
        return normalize_dataframe(pd.read_csv(LOCAL_DATA_PATH, dtype=str).fillna(""))
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)


def write_local_data(df: pd.DataFrame) -> None:
    normalize_dataframe(df).to_csv(LOCAL_DATA_PATH, index=False, encoding="utf-8-sig")


def add_local_record(record: dict[str, Any]) -> None:
    df = load_local_data()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    write_local_data(df)


def add_local_records(records: Iterable[dict[str, Any]]) -> None:
    records = list(records)
    if not records:
        return
    df = load_local_data()
    df = pd.concat([df, pd.DataFrame(records)], ignore_index=True)
    write_local_data(df)


def update_local_record(record_id: str, record: dict[str, Any]) -> None:
    df = load_local_data()
    matches = df.index[df["record_id"].astype(str) == record_id]
    if len(matches) == 0:
        raise StorageError("수정할 기록을 찾지 못했습니다.")
    for column in COLUMNS:
        df.at[matches[0], column] = record.get(column, "")
    write_local_data(df)


def delete_local_record(record_id: str) -> None:
    df = load_local_data()
    df = df[df["record_id"].astype(str) != record_id]
    write_local_data(df)


def backend_info() -> BackendInfo:
    if has_google_secrets():
        return BackendInfo("google", "Google Sheets 연결", "여러 컴퓨터가 같은 데이터를 사용합니다.")
    return BackendInfo("local", "로컬 미리보기", "이 컴퓨터의 CSV에만 저장됩니다. 배포 전 Google Sheets 연결이 필요합니다.")


def load_data() -> pd.DataFrame:
    return load_google_data() if backend_info().mode == "google" else load_local_data()


def add_record(record: dict[str, Any]) -> None:
    if backend_info().mode == "google":
        add_google_record(record)
    else:
        add_local_record(record)


def add_records(records: Iterable[dict[str, Any]]) -> None:
    if backend_info().mode == "google":
        add_google_records(records)
    else:
        add_local_records(records)


def update_record(record_id: str, record: dict[str, Any]) -> None:
    if backend_info().mode == "google":
        update_google_record(record_id, record)
    else:
        update_local_record(record_id, record)


def delete_record(record_id: str) -> None:
    if backend_info().mode == "google":
        delete_google_record(record_id)
    else:
        delete_local_record(record_id)


# ──────────────────────────────────────────────────────────────────────────────
# 로그인
# ──────────────────────────────────────────────────────────────────────────────
def password_gate() -> None:
    configured_password = clean_text(secret_value("app", "app_password", ""))
    if not configured_password:
        return
    password_hash = hashlib.sha256(configured_password.encode("utf-8")).hexdigest()
    if st.session_state.get("authenticated_hash") == password_hash:
        return

    logo_uri = get_logo_data_uri()
    st.markdown(
        f"""
        <div class="owm-hero">
            <img src="{logo_uri}" alt="OWM logo">
            <div><h1>{APP_TITLE}</h1><p>직원용 관리 페이지입니다.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        password = st.text_input("접속 비밀번호", type="password", placeholder="비밀번호 입력")
        submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)
    if submitted:
        attempted_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if attempted_hash == password_hash:
            st.session_state["authenticated_hash"] = password_hash
            st.rerun()
        else:
            st.error("비밀번호가 올바르지 않습니다.")
    st.stop()


password_gate()


# ──────────────────────────────────────────────────────────────────────────────
# 화면 구성
# ──────────────────────────────────────────────────────────────────────────────
def sidebar() -> None:
    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=155)
        st.markdown(f"### {APP_TITLE}")
        st.caption("신사점 인플루언서 응대·방문 기록")
        st.divider()
        info = backend_info()
        if info.mode == "google":
            st.success(f"● {info.label}")
        else:
            st.warning(f"● {info.label}")
        st.caption(info.detail)
        st.divider()
        st.markdown(
            """
            **직원 사용 순서**  
            1. 이름·계정·연락처 검색  
            2. 촬영/기프트 내용 확인  
            3. 촬영 완료 후 직원명과 수령 여부 기록  
            4. 검색되지 않으면 바로 신규 등록
            """
        )
        if st.button("🔄 최신 데이터 불러오기", use_container_width=True):
            safe_rerun()


def hero() -> None:
    logo_uri = get_logo_data_uri()
    st.markdown(
        f"""
        <div class="owm-hero">
            <img src="{logo_uri}" alt="OWM logo">
            <div>
                <h1>{APP_TITLE}</h1>
                <p>{APP_SUBTITLE} · 검색부터 촬영 완료 기록까지 한 화면에서</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(df: pd.DataFrame) -> None:
    today_text = date.today().isoformat()
    today_df = df[df["협찬일"] == today_text] if not df.empty else df
    completed = int((df["진행상태"] == "촬영 완료").sum()) if not df.empty else 0
    pending = int(df["진행상태"].isin(["방문 예정", "촬영 진행"]).sum()) if not df.empty else 0
    gift_pending = int(((df["진행상태"] == "촬영 완료") & (~df["기프트 수령"].map(to_bool))).sum()) if not df.empty else 0
    cols = st.columns(4)
    cols[0].metric("오늘 방문", f"{len(today_df)}명")
    cols[1].metric("진행 중·예정", f"{pending}건")
    cols[2].metric("촬영 완료", f"{completed}건")
    cols[3].metric("기프트 미확인", f"{gift_pending}건")


def record_label(row: pd.Series) -> str:
    account = clean_text(row.get("계정주소"))
    short_account = account.replace("https://www.instagram.com/", "").rstrip("/")
    return f"{clean_text(row.get('협찬일')) or '날짜 미정'} | {clean_text(row.get('방문자명')) or '이름 없음'} | {short_account or '계정 없음'} | {clean_text(row.get('진행상태'))}"


def record_card(row: pd.Series) -> None:
    href = account_href(row.get("계정주소", ""))
    account_html = (
        f'<a class="owm-link" href="{href}" target="_blank">{clean_text(row.get("계정주소"))}</a>'
        if href
        else clean_text(row.get("계정주소")) or "계정 미입력"
    )
    gift_received = "수령 완료" if to_bool(row.get("기프트 수령")) else "미확인"
    st.markdown(
        f"""
        <div class="owm-card">
            <div class="owm-result-title">{clean_text(row.get('방문자명')) or '이름 미입력'}</div>
            <div class="owm-muted">{account_html}</div>
            <div style="margin-top:12px">
                <span class="owm-pill">{clean_text(row.get('진행상태'))}</span>
                <span class="owm-pill">{clean_text(row.get('협찬일')) or '날짜 미정'} {clean_text(row.get('방문 시간'))}</span>
                <span class="owm-pill">{clean_text(row.get('국가')) or '국가 미입력'}</span>
                <span class="owm-pill">기프트 {gift_received}</span>
            </div>
            <hr style="border:0;border-top:1px solid #eee5df;margin:15px 0">
            <p><b>촬영 유형/가이드</b> · {clean_text(row.get('촬영 유형/가이드')) or '-'}</p>
            <p><b>기프트</b> · {clean_text(row.get('기프트')) or '-'}</p>
            <p><b>유료금액</b> · {format_money(row.get('유료금액'))}</p>
            <p><b>연락처</b> · {clean_text(row.get('연락처')) or '-'}</p>
            <p><b>응대직원</b> · {clean_text(row.get('응대직원')) or '-'}</p>
            <p><b>비고</b> · {clean_text(row.get('비고')) or '-'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_record(
    sponsor_date: date,
    visit_time: time,
    country: str,
    account: str,
    visitor_name: str,
    contact: str,
    shoot_type: str,
    gift: str,
    paid_amount: int,
    note: str,
    gift_received: bool,
    staff: str,
    status: str,
    source: str,
    record_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    timestamp = now_text()
    return {
        "record_id": record_id or make_record_id(),
        "협찬일": sponsor_date.isoformat(),
        "방문 시간": visit_time.strftime("%H:%M"),
        "국가": country,
        "계정주소": clean_text(account),
        "방문자명": clean_text(visitor_name),
        "연락처": clean_text(contact),
        "촬영 유형/가이드": clean_text(shoot_type),
        "기프트": clean_text(gift),
        "유료금액": int(paid_amount or 0),
        "비고": clean_text(note),
        "기프트 수령": bool(gift_received),
        "응대직원": clean_text(staff),
        "진행상태": status,
        "등록경로": source,
        "등록일시": created_at or timestamp,
        "최종수정일시": timestamp,
    }


def quick_response_tab(df: pd.DataFrame) -> None:
    st.subheader("🔎 방문자 통합 검색")
    st.caption("기존 명단·카톡 공지·현장 신규 기록을 한 데이터에서 검색합니다.")
    query = st.text_input(
        "이름, 인스타그램 계정, 연락처 검색",
        placeholder="예: @account / 방문자 이름 / 010-0000-0000",
        key="main_search",
    ).strip()

    if query:
        lowered = query.lower()
        mask = pd.Series(False, index=df.index)
        for column in ["방문자명", "계정주소", "연락처", "국가", "비고"]:
            mask = mask | df[column].astype(str).str.lower().str.contains(re.escape(lowered), na=False)
        results = df[mask].copy()
        st.write(f"검색 결과 **{len(results)}건**")
    else:
        today_text = date.today().isoformat()
        results = df[df["협찬일"] == today_text].copy()
        st.write(f"오늘 방문 예정·기록 **{len(results)}건**")

    if not results.empty:
        results = results.sort_values(["협찬일", "방문 시간"], ascending=[False, True])
        options = {record_label(row): row["record_id"] for _, row in results.iterrows()}
        selected_label = st.selectbox("확인할 방문자", list(options.keys()), key="response_selection")
        selected_id = options[selected_label]
        row = df[df["record_id"] == selected_id].iloc[0]
        record_card(row)

        c1, c2, c3 = st.columns([1, 1, 1.4])
        if c1.button("🎬 촬영 시작", type="primary", use_container_width=True, disabled=row["진행상태"] == "촬영 진행"):
            updated = row.to_dict()
            updated["진행상태"] = "촬영 진행"
            updated["최종수정일시"] = now_text()
            update_record(selected_id, updated)
            st.success("촬영 진행 상태로 변경했습니다.")
            safe_rerun()

        with c2.popover("✅ 촬영 완료"):
            with st.form(f"complete_{selected_id}"):
                staff = st.text_input("응대직원", value=clean_text(row["응대직원"]), placeholder="예: 희선")
                gift_received = st.checkbox("기프트 수령 확인", value=to_bool(row["기프트 수령"]))
                extra_note = st.text_area("추가 메모", value=clean_text(row["비고"]), height=100)
                complete = st.form_submit_button("완료 기록 저장", type="primary", use_container_width=True)
            if complete:
                if not staff:
                    st.error("응대직원 이름을 입력해주세요.")
                else:
                    updated = row.to_dict()
                    updated["진행상태"] = "촬영 완료"
                    updated["기프트 수령"] = gift_received
                    updated["응대직원"] = staff
                    updated["비고"] = extra_note
                    updated["최종수정일시"] = now_text()
                    update_record(selected_id, updated)
                    st.success("촬영 완료 기록을 저장했습니다.")
                    safe_rerun()

        if c3.button("✏️ 전체 관리에서 수정", use_container_width=True):
            st.session_state["manage_selected_id"] = selected_id
            st.info("위의 ‘전체 관리’ 탭에서 선택된 기록을 수정할 수 있습니다.")
    else:
        st.info("검색되는 방문자가 없습니다. 아래 버튼으로 바로 신규 등록할 수 있습니다.")
        if st.button("➕ 이 방문자 신규 등록", type="primary"):
            st.session_state["new_prefill"] = query
            st.session_state["open_new_hint"] = True
            st.success("‘신규 등록’ 탭에 검색어를 미리 입력해두었습니다.")

    st.divider()
    st.subheader("📅 오늘 일정")
    today_text = date.today().isoformat()
    today_df = df[df["협찬일"] == today_text].sort_values("방문 시간")
    if today_df.empty:
        st.caption("오늘 등록된 일정이 없습니다.")
    else:
        st.dataframe(
            dataframe_for_display(today_df),
            use_container_width=True,
            hide_index=True,
            column_config={
                "계정주소": st.column_config.LinkColumn("계정주소", display_text=r"https?://(?:www\.)?instagram\.com/(.*?)/?"),
            },
        )


def new_record_tab() -> None:
    st.subheader("➕ 신규 방문·협찬 등록")
    st.caption("명단에 없거나 카톡으로만 공지된 방문자는 여기에서 바로 등록합니다.")
    prefill = clean_text(st.session_state.get("new_prefill", ""))
    account_prefill = prefill if "instagram" in prefill.lower() or prefill.startswith("@") else ""
    name_prefill = "" if account_prefill else prefill

    with st.form("new_record_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        sponsor_date = col1.date_input("협찬일 *", value=date.today())
        visit_time = col2.time_input("방문 시간 *", value=datetime.now().time().replace(second=0, microsecond=0))
        country = col3.selectbox("국가", COUNTRY_OPTIONS)

        col1, col2, col3 = st.columns(3)
        visitor_name = col1.text_input("방문자명 *", value=name_prefill)
        account = col2.text_input("계정주소", value=account_prefill, placeholder="https://www.instagram.com/...")
        contact = col3.text_input("연락처", placeholder="010-0000-0000")

        col1, col2 = st.columns(2)
        shoot_type = col1.text_input("촬영 유형/가이드", placeholder="예: 에피메리 X OWM 유가 / 릴스 1건")
        gift = col2.text_input("기프트", placeholder="예: REJU-ECTO, JUVE-ECTO")

        col1, col2, col3 = st.columns(3)
        paid_amount = col1.number_input("유료금액", min_value=0, step=50000, format="%d")
        status = col2.selectbox("진행상태", STATUS_OPTIONS)
        source = col3.selectbox("등록경로", SOURCE_OPTIONS, index=2)

        col1, col2 = st.columns(2)
        staff = col1.text_input("응대직원", placeholder="방문 전이면 비워도 됩니다")
        gift_received = col2.checkbox("기프트 수령 완료")
        note = st.text_area("비고", placeholder="추가 약속, 피부과 경험, 요청사항 등", height=100)
        submitted = st.form_submit_button("신규 기록 저장", type="primary", use_container_width=True)

    if submitted:
        if not visitor_name and not account:
            st.error("방문자명 또는 계정주소 중 하나는 입력해주세요.")
        else:
            record = build_record(
                sponsor_date,
                visit_time,
                country,
                account,
                visitor_name,
                contact,
                shoot_type,
                gift,
                paid_amount,
                note,
                gift_received,
                staff,
                status,
                source,
            )
            add_record(record)
            st.session_state.pop("new_prefill", None)
            st.success("신규 기록을 저장했습니다.")
            safe_rerun()


def manage_tab(df: pd.DataFrame) -> None:
    st.subheader("🗂️ 전체 관리")
    st.caption("필터로 기록을 찾고, 선택한 행을 수정하거나 삭제할 수 있습니다.")

    f1, f2, f3, f4 = st.columns([1.5, 1, 1, 1])
    keyword = f1.text_input("검색", placeholder="이름·계정·연락처·비고", key="manage_search")
    status_options = ["전체"] + STATUS_OPTIONS
    status_filter = f2.selectbox("진행상태", status_options)
    country_values = sorted({clean_text(x) for x in df["국가"] if clean_text(x)})
    country_filter = f3.selectbox("국가", ["전체"] + country_values)
    date_filter = f4.selectbox("기간", ["전체", "오늘", "향후 일정", "지난 기록"])

    filtered = df.copy()
    if keyword:
        lowered = keyword.lower()
        mask = pd.Series(False, index=filtered.index)
        for column in ["방문자명", "계정주소", "연락처", "비고", "기프트", "촬영 유형/가이드"]:
            mask |= filtered[column].astype(str).str.lower().str.contains(re.escape(lowered), na=False)
        filtered = filtered[mask]
    if status_filter != "전체":
        filtered = filtered[filtered["진행상태"] == status_filter]
    if country_filter != "전체":
        filtered = filtered[filtered["국가"] == country_filter]
    today_text = date.today().isoformat()
    if date_filter == "오늘":
        filtered = filtered[filtered["협찬일"] == today_text]
    elif date_filter == "향후 일정":
        filtered = filtered["협찬일"] >= today_text
    elif date_filter == "지난 기록":
        filtered = filtered["협찬일"] < today_text

    filtered = filtered.sort_values(["협찬일", "방문 시간"], ascending=[False, False])
    st.write(f"표시 중 **{len(filtered)}건** / 전체 {len(df)}건")
    st.dataframe(dataframe_for_display(filtered), use_container_width=True, hide_index=True, height=360)

    if filtered.empty:
        return

    options = {record_label(row): row["record_id"] for _, row in filtered.iterrows()}
    preferred = st.session_state.pop("manage_selected_id", None)
    default_index = 0
    if preferred and preferred in options.values():
        default_index = list(options.values()).index(preferred)
    selected_label = st.selectbox("수정할 기록 선택", list(options.keys()), index=default_index, key="manage_selection")
    selected_id = options[selected_label]
    row = df[df["record_id"] == selected_id].iloc[0]

    with st.expander("선택 기록 수정", expanded=True):
        with st.form(f"edit_form_{selected_id}"):
            parsed_date = pd.to_datetime(row["협찬일"], errors="coerce")
            date_value = parsed_date.date() if not pd.isna(parsed_date) else date.today()
            parsed_time = pd.to_datetime(row["방문 시간"], errors="coerce")
            time_value = parsed_time.time().replace(second=0, microsecond=0) if not pd.isna(parsed_time) else time(12, 0)

            c1, c2, c3 = st.columns(3)
            sponsor_date = c1.date_input("협찬일", value=date_value, key=f"edit_date_{selected_id}")
            visit_time = c2.time_input("방문 시간", value=time_value, key=f"edit_time_{selected_id}")
            current_country = clean_text(row["국가"])
            country_choices = list(dict.fromkeys(COUNTRY_OPTIONS + ([current_country] if current_country else [])))
            country = c3.selectbox(
                "국가",
                country_choices,
                index=country_choices.index(current_country) if current_country in country_choices else 0,
                key=f"edit_country_{selected_id}",
            )

            c1, c2, c3 = st.columns(3)
            visitor_name = c1.text_input("방문자명", value=clean_text(row["방문자명"]), key=f"edit_name_{selected_id}")
            account = c2.text_input("계정주소", value=clean_text(row["계정주소"]), key=f"edit_account_{selected_id}")
            contact = c3.text_input("연락처", value=clean_text(row["연락처"]), key=f"edit_contact_{selected_id}")

            c1, c2 = st.columns(2)
            shoot_type = c1.text_input("촬영 유형/가이드", value=clean_text(row["촬영 유형/가이드"]), key=f"edit_shoot_{selected_id}")
            gift = c2.text_input("기프트", value=clean_text(row["기프트"]), key=f"edit_gift_{selected_id}")

            c1, c2, c3 = st.columns(3)
            paid_amount = c1.number_input("유료금액", min_value=0, step=50000, value=normalize_money(row["유료금액"]), key=f"edit_paid_{selected_id}")
            current_status = clean_text(row["진행상태"]) or "방문 예정"
            status = c2.selectbox("진행상태", STATUS_OPTIONS, index=STATUS_OPTIONS.index(current_status) if current_status in STATUS_OPTIONS else 0, key=f"edit_status_{selected_id}")
            current_source = clean_text(row["등록경로"]) or "기타"
            source_choices = list(dict.fromkeys(SOURCE_OPTIONS + [current_source]))
            source = c3.selectbox("등록경로", source_choices, index=source_choices.index(current_source), key=f"edit_source_{selected_id}")

            c1, c2 = st.columns(2)
            staff = c1.text_input("응대직원", value=clean_text(row["응대직원"]), key=f"edit_staff_{selected_id}")
            gift_received = c2.checkbox("기프트 수령 완료", value=to_bool(row["기프트 수령"]), key=f"edit_received_{selected_id}")
            note = st.text_area("비고", value=clean_text(row["비고"]), height=100, key=f"edit_note_{selected_id}")

            save = st.form_submit_button("수정사항 저장", type="primary", use_container_width=True)

        if save:
            updated = build_record(
                sponsor_date,
                visit_time,
                country,
                account,
                visitor_name,
                contact,
                shoot_type,
                gift,
                paid_amount,
                note,
                gift_received,
                staff,
                status,
                source,
                record_id=selected_id,
                created_at=clean_text(row["등록일시"]) or now_text(),
            )
            update_record(selected_id, updated)
            st.success("수정사항을 저장했습니다.")
            safe_rerun()

        st.warning("삭제하면 되돌릴 수 없습니다. CSV 백업 후 삭제하는 것을 권장합니다.")
        confirm = st.checkbox("이 기록을 삭제하는 데 동의합니다", key=f"delete_confirm_{selected_id}")
        if st.button("🗑️ 선택 기록 삭제", disabled=not confirm, key=f"delete_button_{selected_id}"):
            delete_record(selected_id)
            st.success("기록을 삭제했습니다.")
            safe_rerun()


def data_tab(df: pd.DataFrame) -> None:
    st.subheader("📥 기존 시트 가져오기 · 백업")
    st.caption("기존 구글시트를 CSV로 내려받아 업로드하면 통합 관리 데이터에 추가할 수 있습니다.")

    export_name = f"OWM_인플루언서_백업_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    st.download_button(
        "⬇️ 전체 데이터 CSV 백업",
        data=csv_bytes(df),
        file_name=export_name,
        mime="text/csv",
        use_container_width=True,
    )

    st.divider()
    upload = st.file_uploader("기존 시트 CSV 업로드", type=["csv"])
    skip_duplicates = st.checkbox("기존 데이터와 중복되는 행은 건너뛰기", value=True)

    if upload is not None:
        try:
            raw = upload.getvalue()
            try:
                raw_df = pd.read_csv(io.BytesIO(raw), dtype=str, encoding="utf-8-sig").fillna("")
            except UnicodeDecodeError:
                raw_df = pd.read_csv(io.BytesIO(raw), dtype=str, encoding="cp949").fillna("")
            imported = import_dataframe(raw_df)
            st.write(f"가져올 수 있는 행: **{len(imported)}건**")
            st.dataframe(dataframe_for_display(imported.head(20)), use_container_width=True, hide_index=True)

            if st.button("CSV 데이터를 통합 관리에 추가", type="primary", use_container_width=True):
                to_add = imported.copy()
                if skip_duplicates and not df.empty:
                    existing_keys = {
                        (
                            clean_text(row["협찬일"]),
                            clean_text(row["방문자명"]).lower(),
                            clean_text(row["계정주소"]).lower(),
                        )
                        for _, row in df.iterrows()
                    }
                    mask = []
                    for _, row in to_add.iterrows():
                        key = (
                            clean_text(row["협찬일"]),
                            clean_text(row["방문자명"]).lower(),
                            clean_text(row["계정주소"]).lower(),
                        )
                        mask.append(key not in existing_keys)
                    to_add = to_add[pd.Series(mask, index=to_add.index)]
                add_records(to_add.to_dict("records"))
                skipped = len(imported) - len(to_add)
                st.success(f"{len(to_add)}건을 추가했습니다. 중복으로 건너뛴 행: {skipped}건")
                safe_rerun()
        except Exception as exc:
            st.error(f"CSV를 읽지 못했습니다: {exc}")

    st.divider()
    with st.expander("CSV 열 이름 안내"):
        st.write(
            "협찬일, 방문 시간, 국가, 계정주소, 방문자명, 연락처, 촬영 유형/가이드, "
            "기프트, 유료금액, 비고, 기프트 수령, 응대직원 열을 자동으로 인식합니다. "
            "띄어쓰기나 ‘촬영 유형 선택/가이드’ 같은 기존 표기도 함께 인식합니다."
        )


def main() -> None:
    sidebar()
    hero()
    try:
        df = ensure_unique_record_ids(load_data())
    except StorageError as exc:
        st.error(str(exc))
        st.info("README.md의 Google Sheets 연결 안내와 Streamlit Secrets 설정을 확인해주세요.")
        st.stop()
    except Exception as exc:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {exc}")
        st.stop()

    render_metrics(df)
    st.write("")
    tab_response, tab_new, tab_manage, tab_data = st.tabs(
        ["✨ 방문 응대", "➕ 신규 등록", "🗂️ 전체 관리", "📥 CSV·백업"]
    )
    with tab_response:
        quick_response_tab(df)
    with tab_new:
        new_record_tab()
    with tab_manage:
        manage_tab(df)
    with tab_data:
        data_tab(df)

    st.caption("OWM Influencer Desk · 데이터 변경 시 최종수정일시가 자동 기록됩니다.")


if __name__ == "__main__":
    main()
