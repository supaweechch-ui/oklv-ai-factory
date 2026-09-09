"""AI agent 2: turn a campaign plan into production-ready visual prompts."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Campaign, VisualPromptPack

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


def create_visual_prompts(campaign: Campaign) -> VisualPromptPack:
    """Generate one consistent image/video prompt package for every scene."""
    scenes_text = "\n\n".join(
        f"""SCENE {scene.scene_number}
Duration: {scene.duration_seconds} seconds
Purpose: {scene.purpose}
Description: {scene.description}
Dialogue: {scene.dialogue}"""
        for scene in campaign.scenes
    )

    prompt = f"""
คุณคือ AI Prompt Engineer ระดับมืออาชีพสำหรับโฆษณา AI Video แบบ cinematic

ข้อมูลแคมเปญ
สินค้า: {campaign.product}
กลุ่มเป้าหมาย: {campaign.target_audience}
Concept: {campaign.concept}
Key message: {campaign.key_message}
Tone: {campaign.tone}

Scenes:
{scenes_text}

สร้าง prompt สำหรับทุกฉาก โดยมี 4 prompts พอดี เรียง scene_number 1 ถึง 4
- image_prompt และ video_prompt เขียนภาษาอังกฤษเพื่อใช้กับเครื่องมือสร้างภาพ/วิดีโอ
- ภาพเป็น cinematic vertical advertising, 9:16
- ระบุ subject, action, setting, product placement, camera motion และแสงให้ชัดเจน
- character_consistency ต้องอธิบายรูปลักษณ์ เสื้อผ้า และตัวสินค้าเดียวกันทุกฉาก
- หลีกเลี่ยงตัวอักษร โลโก้ที่อ่านได้ และองค์ประกอบที่สร้างยากเกินจำเป็น
- ห้ามเปลี่ยนสินค้าเป็นสินค้าอื่น หรือใส่คำกล่าวอ้างที่เกินจริง
- production_notes เป็นคำแนะนำสั้น ๆ ภาษาไทยสำหรับผู้ตัดต่อ
"""

    client = _client()
    response = client.models.generate_content(
        model=_model_name(),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": VisualPromptPack,
        },
    )
    print("กำลังตรวจสอบ Visual Prompts ที่ AI สร้าง...", flush=True)
    return VisualPromptPack.model_validate(response.parsed)
