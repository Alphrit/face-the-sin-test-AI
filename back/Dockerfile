# 1. 사용할 파이썬 버전
FROM python:3.12-slim

# 2. 컨테이너 내부의 작업 폴더를 /app으로 지정
WORKDIR /app

# 3. 필요한 라이브러리 목록(requirements.txt)을 먼저 복사
COPY requirements.txt .

# 4. 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 현재 폴더(back)의 모든 코드(main.py, data 등)를 컨테이너 안으로 복사
COPY . .

# 6. FastAPI가 사용할 8000 포트를 열어둠
EXPOSE 8000

# 7. 컨테이너가 켜질 때 실행할 명령어 (uvicorn으로 main.py의 app 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]