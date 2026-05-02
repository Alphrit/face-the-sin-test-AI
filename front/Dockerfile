# 1. 사용할 파이썬 버전 (기존에 쓰시던 3.12 버전의 가벼운 slim 버전 사용)
FROM python:3.12-slim

# 2. 컨테이너 내부의 작업 폴더를 /app으로 지정
WORKDIR /app

# 3. 필요한 라이브러리 목록(requirements.txt)을 먼저 복사
COPY requirements.txt .

# 4. 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 현재 폴더(front)의 모든 코드(app.py, images, data 등)를 컨테이너 안으로 복사
COPY . .

# 6. Streamlit이 사용할 8501 포트를 열어둠
EXPOSE 8501

# 7. 컨테이너가 켜질 때 실행할 명령어
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]