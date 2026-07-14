# OWM Influencer Desk

옵티마웰니스 신사점의 인플루언서 방문 확인, 촬영 진행, 제품 증정, 응대직원 기록을 한 화면에서 관리하는 Streamlit 앱입니다.

## 주요 기능

- 이름·인스타그램 계정·연락처 통합 검색
- 오늘 방문 일정 확인
- 촬영 시작 / 촬영 완료 상태 변경
- 기프트 수령 여부와 응대직원 기록
- 신규 방문자 등록
- 전체 기록 필터·수정·삭제
- 기존 구글시트 CSV 가져오기
- 전체 데이터 CSV 백업
- Google Sheets를 데이터베이스처럼 사용하여 여러 컴퓨터에서 동일 데이터 공유
- 선택형 직원 접속 비밀번호

## GitHub에 올릴 파일

저장소 루트가 아래 구조가 되도록 **이 폴더 안의 파일을 전부** 올리세요.

```text
OWM_Influencer_Streamlit/
├─ app.py
├─ requirements.txt
├─ README.md
├─ SETUP_GUIDE_KR.md
├─ sample_data.csv
├─ assets/
│  └─ owm_logo_transparent.png
├─ data/
│  └─ .gitkeep
└─ .streamlit/
   ├─ config.toml
   └─ secrets.toml.example
```

`secrets.toml`은 비밀번호와 Google 키가 들어가므로 GitHub에 올리면 안 됩니다. `.gitignore`가 이를 막도록 설정되어 있습니다.

## 로컬 실행

Python 3.11 또는 3.12 환경을 권장합니다.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Google Sheets 설정 전에는 로컬 CSV 미리보기 모드로 실행됩니다. 이 모드는 개발 확인용이며, Streamlit Community Cloud에서 영구 저장용으로 사용하면 안 됩니다.

## 실제 운영 권장 구성

```text
직원 브라우저 → Streamlit 앱 → Google Sheets 통합 관리 시트
```

Google Sheets 연결 및 Streamlit 배포 과정은 `SETUP_GUIDE_KR.md`를 따라 하면 됩니다.
