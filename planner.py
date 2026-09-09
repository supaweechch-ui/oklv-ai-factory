"""AI agent 1: create a structured short-form video campaign."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Campaign

load_dotenv()


def _client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ไม่พบ GEMINI_API_KEY ในไฟล์ .env — เพิ่ม GEMINI_API_KEY=your_key แล้วลองใหม่"
        )
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=60_000,
            retry_options=types.HttpRetryOptions(
                attempts=2,
                initial_delay=1,
                max_delay=3,
            ),
        ),
    )


def _model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def create_campaign(product: str, target: str, selling_point: str) -> Campaign:
    """Return a four-scene, approximately 30-second advertisement plan."""
    prompt = f"""
คุณคือ Creative Director มืออาชีพด้านโฆษณา Short-form Video

สร้างแคมเปญโฆษณาจากข้อมูลต่อไปนี้
สินค้า: {product}
กลุ่มเป้าหมาย: {target}
จุดขาย: {selling_point}

ข้อกำหนด:
- ความยาวรวมประมาณ 30 วินาที
- ต้องมี 4 ฉากพอดี และเรียง scene_number ตั้งแต่ 1 ถึง 4
- เหตุการณ์ สถานที่ ตัวละคร และภาพลักษณ์สินค้า ต้องต่อเนื่องกัน
- สินค้าเป็นส่วนสำคัญของเรื่องทุกฉาก
- ทุกฉากต้องนำไปสร้างภาพและวิดีโอด้วย AI ได้จริง จึงหลีกเลี่ยงรายละเอียดซับซ้อน
- เขียน dialogue เป็นภาษาไทย กระชับและเหมาะกับโฆษณา
- อย่าอ้างสรรพคุณที่พิสูจน์ไม่ได้หรือทำให้เข้าใจผิด
"""

    client = _client()
    response = client.models.generate_content(
        model=_model_name(),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Campaign,
        },
    )
    print("กำลังตรวจสอบแผนโฆษณาที่ AI สร้าง...", flush=True)
    return Campaign.model_validate(response.parsed)
