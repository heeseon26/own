# OWM Influencer Desk 설치·배포 가이드

## 1. 새 Google Sheet 준비

1. Google Drive에서 새 스프레드시트를 만듭니다.
2. 이름은 예를 들어 `OWM 인플루언서 통합관리`로 지정합니다.
3. 시트 탭을 미리 만들 필요는 없습니다. 앱이 `OWM_통합관리` 탭과 열 제목을 자동 생성합니다.
4. 주소창에서 아래 부분을 복사합니다.

```text
https://docs.google.com/spreadsheets/d/여기가_spreadsheet_id/edit
```

## 2. Google Cloud 서비스 계정 만들기

1. Google Cloud Console에서 프로젝트를 하나 만듭니다.
2. `Google Sheets API`와 `Google Drive API`를 활성화합니다.
3. `IAM 및 관리자 → 서비스 계정`에서 서비스 계정을 만듭니다.
4. 서비스 계정의 `키 → 키 추가 → 새 키 만들기 → JSON`을 선택해 JSON 키를 내려받습니다.
5. JSON 안의 `client_email` 주소를 복사합니다.
6. 1번에서 만든 Google Sheet의 공유 버튼을 누르고, 이 `client_email`을 **편집자**로 초대합니다.

> JSON 파일과 private key는 카톡, 노션 공개 페이지, GitHub에 올리지 마세요.

## 3. 내 컴퓨터에서 Secrets 설정

`.streamlit/secrets.toml.example`을 복사하여 같은 폴더에 `secrets.toml`로 만듭니다.

```text
.streamlit/
├─ config.toml
├─ secrets.toml.example
└─ secrets.toml   ← 실제 비밀값, GitHub 업로드 금지
```

JSON 파일의 값을 `secrets.toml`에 옮깁니다. `private_key`는 BEGIN/END 줄을 포함해 그대로 넣습니다.

```toml
[app]
spreadsheet_id = "복사한 spreadsheet_id"
worksheet_name = "OWM_통합관리"
app_password = "약국 직원이 사용할 비밀번호"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
client_email = "...iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

`app_password = ""`처럼 비워두면 앱 자체 비밀번호 화면은 나오지 않습니다.

## 4. GitHub 저장소 만들기

1. GitHub에서 새 저장소를 만듭니다. 예: `owm-influencer-desk`
2. 이 폴더의 파일을 전부 업로드합니다.
3. `.streamlit/secrets.toml`이 올라가지 않았는지 반드시 확인합니다.
4. `.streamlit/secrets.toml.example`은 예시 파일이므로 올려도 됩니다.

터미널로 올릴 때:

```bash
git init
git add .
git commit -m "feat: add OWM influencer desk"
git branch -M main
git remote add origin https://github.com/내아이디/owm-influencer-desk.git
git push -u origin main
```

## 5. Streamlit Community Cloud 배포

1. Streamlit Community Cloud에 GitHub 계정으로 로그인합니다.
2. `Create app` 또는 `New app`을 누릅니다.
3. GitHub 저장소, `main` 브랜치, 진입 파일 `app.py`를 선택합니다.
4. Advanced settings의 Python 버전은 로컬과 같은 버전을 선택합니다. 권장: Python 3.11 또는 3.12.
5. Secrets 입력칸에 로컬의 `.streamlit/secrets.toml` **내용만** 붙여넣습니다.
6. Deploy를 누릅니다.

배포 후 생성되는 주소 예시:

```text
https://owm-influencer-desk.streamlit.app
```

이 주소를 약국 메인 컴퓨터 크롬 북마크의 `인플루언서` 폴더에 저장하면 됩니다.

## 6. 기존 스프레드시트 데이터 옮기기

1. 기존 인플루언서 시트를 엽니다.
2. `파일 → 다운로드 → 쉼표로 구분된 값(.csv)`을 선택합니다.
3. OWM 앱의 `CSV·백업` 탭에서 CSV를 업로드합니다.
4. 미리보기와 건수를 확인한 후 `CSV 데이터를 통합 관리에 추가`를 누릅니다.
5. 중복 방지 옵션은 기본적으로 켜져 있습니다.

다음 열 이름은 자동 인식합니다.

- 협찬일
- 방문 시간 또는 방문시간
- 국가
- 계정주소
- 방문자명
- 연락처
- 촬영 유형 선택/가이드 또는 촬영 유형/가이드
- 기프트
- 유료금액
- 비고
- 기프트 수령
- 응대직원

## 7. 실제 사용 전 확인 목록

- 샘플 데이터가 아닌 실제 Google Sheet에 연결되었는지
- 서비스 계정 이메일이 시트 편집자로 공유되었는지
- 직원 비밀번호가 설정되었는지
- 약국 컴퓨터와 개인 휴대폰에서 같은 데이터가 보이는지
- 신규 등록, 촬영 시작, 촬영 완료, 수정, CSV 백업이 모두 작동하는지
- 개인정보가 있으므로 앱 주소와 비밀번호를 외부에 공유하지 않았는지

## 문제 해결

### `SpreadsheetNotFound`

- spreadsheet_id가 올바른지 확인합니다.
- Google Sheet를 서비스 계정의 client_email에 편집자로 공유했는지 확인합니다.

### `Google Sheets 연결 실패`

- Streamlit Secrets의 private_key 줄바꿈이 유지되었는지 확인합니다.
- Google Sheets API와 Google Drive API가 활성화되었는지 확인합니다.

### 배포 후 수정 내용이 반영되지 않음

- GitHub의 main 브랜치에 push되었는지 확인합니다.
- Streamlit 앱 메뉴에서 Reboot app을 실행합니다.

### 앱이 공개 주소라 개인정보가 걱정됨

- 이 앱의 `app_password`를 반드시 설정합니다.
- 가능하다면 Streamlit 앱 자체도 비공개 공유 설정을 사용합니다.
- 정기적으로 CSV 백업을 내려받아 별도 보관합니다.
