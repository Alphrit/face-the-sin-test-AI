from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import google.generativeai as genai
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def load_excel_rules():
    try:
        df = pd.read_excel("data/수감자 죄악.xlsx", sheet_name="소속")
        return df.to_string(index=False)
    except Exception as e:
        logger.error(f"엑셀 로드 실패: {e}")
        return "데이터를 불러올 수 없습니다."

knowledge_base = load_excel_rules()
class UserInput(BaseModel):
    scores: dict

@app.post("/recommend")
async def get_recommendation(user_input: UserInput):
    sin_scores = {k: v for k, v in user_input.scores.items() if k not in ["손가락", "날개"]}
    tendency = {k: v for k, v in user_input.scores.items() if k in ["손가락", "날개"]}

    prompt = f"""
    너는 '프로젝트문' 세계관의 전문 분석가야. 
    유저의 [죄악 점수]와 [성향 지수]를 분석해서, 가장 잘 어울리는 [소속]을 하나 추천해줘.

    [소속 데이터베이스]
    (각 소속 옆의 '분류'는 해당 소속이 날개(둥지/협회)인지 손가락(뒷골목/조직)인지를 나타냄)
    {knowledge_base}

    [유저 데이터]
    1. 죄악 점수: {sin_scores}
    2. 성향 지수 (경향성): {tendency}

    [판정 가이드라인]
    - '죄악 점수'의 패턴이 해당 소속의 핵심 스킬/성향과 일치하는지가 가장 중요해.
    - '성향 지수'는 절대적인 필터가 아니라 **'우선순위 가중치'**로 사용해줘.
    - 예를 들어, 유저의 '날개' 지수가 '손가락'보다 높다면, 가급적 [날개] 분류의 소속 중에서 우선적으로 검토하되, 
      죄악 점수가 [손가락] 쪽 조직과 너무나도 완벽하게 일치한다면 그쪽을 선택해도 좋아.
    - 결과는 반드시 아래 JSON 형식으로만 답해줘.

    {{
        "recommended_faction": "소속 이름",
        "reason": "죄악 점수와 날개/손가락 성향이 어떻게 조화를 이루어 이 결과가 나왔는지 세계관에 몰입하여 3~4문장으로 설명."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(raw_text)
    except Exception as e:
        logger.error(f"추천 생성 실패: {e}")
        return {"recommended_faction": "도시의 유랑자", "reason": "분석 장치에 과부하가 걸렸습니다."}