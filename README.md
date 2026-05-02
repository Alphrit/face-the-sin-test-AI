# Face the Sin : 도시 생존 성향 테스트
프로젝트문의 세계관을 바탕으로, 사용자의 성향과 죄악 속성을 분석하여 가장 잘 어울리는 소속을 판별해 주는 Streamlit 기반 웹 애플리케이션입니다.
AWS EC2 환경에 실제 배포되어 누적 2,400회 이상의 테스트 진행 및 300개가 넘는 커뮤니티 댓글 반응을 이끌어낸 성공적인 운영 경험이 담긴 프로젝트입니다.

## 개발자 정보
- **학번**: 2021204045
- **이름**: 이성민

## 주요 기능 및 트러블슈팅
1. **동시성 제어 및 무중단 운영**

실제 서비스 배포 후 다수의 유저가 동시에 테스트 결과를 저장하면서 JSON 파일이 깨지는 **동시성 오류(Concurrency Issue)**가 발생했습니다.

이를 해결하기 위해 filelock 라이브러리를 도입, 파일 쓰기 작업 시 락(Lock)을 걸어 순차적으로 데이터를 처리하도록 로직을 전면 수정하여 안정적인 서버 환경을 구축했습니다.

2. **Admin 대시보드 및 통계 시스템**

유저들의 테스트 데이터를 실시간으로 수집하여 global_stats.json에 저장합니다.

Admin 계정 로그인 시, 각 문항별 유저들의 선택 비율과 누적 테스트 완료 횟수를 시각적으로 확인할 수 있는 관리자 전용 대시보드를 제공합니다.

3. **로그인 및 회원가입** (auth.py)

Pandas를 활용하여 data/users.csv에 회원 정보를 관리합니다.

보안을 위해 사용자 비밀번호는 SHA-256 해시 함수를 통해 안전하게 암호화하여 저장합니다.

4. **퀴즈 및 알고리즘 최적화** (@st.cache_data)

엑셀(수감자 죄악.xlsx) 데이터베이스를 기반으로 사용자의 7대 죄악 비율(%)과 소속별 죄악 비율의 거리를 계산하여 최적의 파벌을 매핑합니다.

방대한 퀴즈 문항(questions.json)과 결과 계산 로직에 Streamlit 캐싱을 적용하여 페이지 로딩 속도를 최적화했습니다.

## 기술 스택
Language: Python 3.12

Frontend/Backend: Streamlit

Deployment: AWS EC2 (Ubuntu), Elastic IP 고정

Database (File-based): JSON, CSV

Key Libraries: pandas, filelock

## 실행 및 배포 방법
[로컬 환경에서 실행]
1. 저장소 클론 및 폴더 이동

```bash
git clone https://github.com/Alphrit/face-the-sin-test
cd face-the-sin-test
```
2. 필수 라이브러리 설치 (가상환경 venv 사용 권장)
```bash
pip install -r requirements.txt
```
3. 애플리케이션 실행

```bash
streamlit run app.py
```
## [AWS EC2 서버 환경 배포]
터미널 종료 후에도 서버가 24시간 백그라운드에서 동작하도록 아래 명령어를 사용하여 실행합니다.

```bash
nohup streamlit run app.py &
```
## 프로젝트 구조
```plaintext
face-the-sin-test
 ┣ data/
 ┃ ┣ global_stats.json    # (자동생성) 전체 유저 선택 통계 데이터
 ┃ ┣ history_*.json       # (자동생성) 유저 및 비회원별 테스트 기록
 ┃ ┣ questions.json       # 퀴즈 문항 및 선택지 데이터
 ┃ ┣ users.csv            # (자동생성) 회원가입 및 암호화 데이터
 ┃ ┗ 수감자 죄악.xlsx     # 결과 매핑 알고리즘용 엑셀 데이터
 ┣ images/                # UI용 배경, 로고, 캐릭터 이미지 폴더
 ┣ app.py                 # Streamlit 메인 실행 파일 및 뷰
 ┣ auth.py                # 로그인/회원가입 처리 및 암호화 모듈
 ┣ .gitignore             # Git 제외 파일 목록
 ┣ requirements.txt       # 필수 라이브러리 목록
 ┗ README.md              # 프로젝트 설명서 (현재 파일)
 ```