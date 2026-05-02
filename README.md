# Face the Sin : 도시 생존 성향 테스트 (AI 기반 추천 시스템)
- 2026학년도 1학기 오픈소스소프트웨어실습 기말고사 대체 과제

프로젝트문의 세계관을 바탕으로, 사용자의 7대 죄악 속성과 경향성을 분석하여 가장 잘 어울리는 소속을 추천해 주는 **AI 기반 추천 웹 애플리케이션**입니다.
기존의 단순 수학적 연산 기반 테스트(누적 2,400회 이상 테스트 진행)를 발전시켜, Streamlit(프론트엔드) + FastAPI(백엔드) + Docker + AWS EC2 기반의 MSA(마이크로서비스 아키텍처) 구조로 전면 개편하고 Gemini 2.5 Flash API를 연동하여 지능형 추천 엔진을 구현했습니다.

개발자 정보
- 학번: 2021204045
- 이름: 이성민

**배포 주소**(EC2): http://34.237.195.172:8503

## 시스템 아키텍처
**사용자 입력** (Streamlit): 유저가 퀴즈를 풀며 7대 죄악 및 날개/손가락 경향성 점수를 누적합니다.
**API 호출** (HTTP 통신): Streamlit이 최종 합산된 점수 JSON을 FastAPI 백엔드 엔드포인트(/recommend)로 POST 전송합니다.
**추천 로직** (FastAPI + Gemini AI): FastAPI가 엑셀 데이터베이스(수감자 죄악.xlsx)의 소속별 가중치 기준표와 유저의 점수를 결합하여 Gemini 2.5 Flash API에 프롬프트로 전달, 가장 적합한 소속과 그 이유를 추론하여 JSON 형태로 반환합니다.

**결과 출력** (Streamlit): 백엔드로부터 받은 추천 결과를 파싱하여 시각적인 UI와 함께 화면에 렌더링합니다.

**실행 환경** (Docker & EC2): Front와 Back을 독립된 Docker 컨테이너로 분리하였으며, AWS EC2 환경에서 docker-compose를 통해 무중단 배포되었습니다.

**주요 기능 및 트러블슈팅**
1. **지능형 추천 엔진** (FastAPI + LLM 도입)
기존 무조건적으로 세력을 양분하는 로직과 달리, 날개 지수와 손가락 지수를 가중치로 활용하는 프롬프트 엔지니어링을 적용했습니다. 이를 통해 점수가 일치하더라도 유저의 성향에 따라 '리우협회' 혹은 '중지' 등 세계관에 완벽히 몰입할 수 있는 입체적이고 유연한 추천 결과를 제공합니다.

2. **컨테이너 분리 및 통신 오류 해결** (Docker)
Streamlit과 FastAPI를 각각의 컨테이너로 분리(docker-compose.yml)하고 depends_on 옵션을 부여하여 실행 순서를 제어했습니다. 네트워크 환경 분리로 인해 발생할 수 있는 내부 통신 에러를 포트 포워딩(8503:8501, 8001:8000)으로 안정적으로 해결했습니다.

3. **동시성 제어 및 통계 대시보드** (FileLock)
다수의 유저가 동시에 접속하여 global_stats.json에 데이터를 기록할 때 발생하는 파일 손상 오류를 방지하기 위해 filelock 라이브러리를 적용했습니다. 이를 기반으로 Admin 계정 로그인 시 전체 유저의 선택 트렌드를 볼 수 있는 대시보드를 제공합니다.

4. **보안 및 회원 관리** (Auth & .env)
보안을 위해 유저의 비밀번호는 SHA-256 해시 함수로 암호화되어 users.csv에 저장되며, API 키(GEMINI_API_KEY)는 .gitignore로 제외된 서버 내부의 .env 파일을 통해 안전하게 Docker 컨테이너로 주입됩니다.

## 기술 스택
- Language: Python 3.12
- Frontend: Streamlit
- Backend: FastAPI, Uvicorn
- AI / LLM: Google Generative AI (Gemini 2.5 Flash)
- Deployment: Docker, Docker Compose, AWS EC2 (Ubuntu)
- Data & Security: Pandas, FileLock, hashlib (SHA-256)

## 실행 및 배포 방법
**[사전 준비]**
프로젝트 루트 디렉토리에 .env 파일을 생성하고 Gemini API 키를 입력합니다. 본 Github 서버에는 존재하지 않지만, EC2 서버 안에 따로 .env 파일을 생성하였습니다.
```plaintext
GEMINI_API_KEY=my_key
```
[Docker 기반 통합 실행 (권장/EC2 환경)]
1. 저장소 클론 및 폴더 이동
```bash
git clone https://github.com/Alphrit/face-the-sin-test-AI
cd face-the-sin-test-AI
```
2. Docker Compose를 통한 백그라운드 빌드 및 실행
```bash
sudo docker-compose up -d --build
```
3. 접속
- Frontend: http://34.237.195.172:8503/
- Backend Swagger Docs: http://34.237.195.172:8001/docs

프로젝트 구조
```plaintext
FACE-THE-SIN-AI/
 ┣ back/                  # FastAPI 백엔드 디렉토리
 ┃ ┣ data/
 ┃ ┃ ┗ 수감자 죄악.xlsx    # AI 프롬프트 분석용 기준 데이터
 ┃ ┣ Dockerfile           # 백엔드용 도커 파일
 ┃ ┣ main.py              # FastAPI 엔드포인트 및 Gemini API 호출 로직
 ┃ ┗ requirements.txt
 ┣ front/                 # Streamlit 프론트엔드 디렉토리
 ┃ ┣ data/
 ┃ ┃ ┣ global_stats.json  # 유저 선택 통계 데이터
 ┃ ┃ ┣ questions.json     # 퀴즈 문항 및 선택지 데이터
 ┃ ┃ ┗ users.csv          # (보안) 암호화된 회원 정보
 ┃ ┣ images/              # UI 리소스 (배경, 캐릭터 등)
 ┃ ┣ app.py               # Streamlit 메인 UI 및 백엔드 통신 로직
 ┃ ┣ auth.py              # 회원가입/로그인 및 암호화 모듈
 ┃ ┣ Dockerfile           # 프론트엔드용 도커 파일
 ┃ ┗ requirements.txt
 ┣ .env                   # (Git 제외) API Key 및 환경 변수
 ┣ .gitignore             # 로그 및 개인정보 파일 제외 목록
 ┣ docker-compose.yml     # Front/Back 컨테이너 통합 실행 설정
 ┗ README.md              # 프로젝트 설명서 (현재 파일)
```
