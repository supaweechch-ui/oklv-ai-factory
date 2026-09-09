"""Command-line entry point for OKLV AI Factory."""

import json
import sys
from datetime import datetime
from pathlib import Path

from google.genai.errors import APIError
from httpx import RequestError
from pydantic import ValidationError

from planner import create_campaign
from prompt_engine import create_visual_prompts


def _configure_utf8_console() -> None:
    """Keep Thai prompts readable in Windows terminals and redirected output."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def _required_input(label: str) -> str:
    value = input(label).strip()
    if not value:
        raise ValueError("กรุณากรอกข้อมูลให้ครบ")
    return value


def _save_output(campaign, visual_prompts) -> Path:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    filename = datetime.now().strftime("campaign_%Y%m%d_%H%M%S.json")
    output_path = output_dir / filename
    output_path.write_text(
        json.dumps(
            {
                "campaign": campaign.model_dump(),
                "visual_prompts": visual_prompts.model_dump(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    _configure_utf8_console()
    print("=" * 60)
    print("                 OKLV AI FACTORY")
    print("=" * 60)

    try:
        product = _required_input("\nสินค้า: ")
        target = _required_input("กลุ่มเป้าหมาย: ")
        selling_point = _required_input("จุดขาย: ")

        print("\n🧠 AI #1 กำลังวางแผนโฆษณา...")
        campaign = create_campaign(product, target, selling_point)
        print("✅ AI #1 เสร็จแล้ว")
        print(f"\nConcept: {campaign.concept}")
        print(f"จำนวนฉาก: {len(campaign.scenes)}")

        print("\n🎨 AI #2 กำลังสร้าง Visual Prompts...")
        visual_prompts = create_visual_prompts(campaign)
        output_path = _save_output(campaign, visual_prompts)

        print("✅ AI #2 เสร็จแล้ว")
        print(f"\nบันทึกผลลัพธ์แล้ว: {output_path}")
        for item in visual_prompts.prompts:
            print(f"\n--- Scene {item.scene_number} ---")
            print(f"Image prompt: {item.image_prompt}")
            print(f"Video prompt: {item.video_prompt}")
    except APIError as error:
        print("\nเชื่อมต่อ Gemini API ไม่สำเร็จ")
        print("ตรวจสอบว่า GEMINI_API_KEY ในไฟล์ .env ถูกต้องและยังใช้งานได้")
        print(f"รายละเอียด: {error}")
    except RequestError:
        print("\nเชื่อมต่อ Gemini API ไม่ได้")
        print("ตรวจสอบอินเทอร์เน็ต, DNS, VPN หรือ firewall แล้วลองใหม่อีกครั้ง")
    except (RuntimeError, ValueError, ValidationError) as error:
        print(f"\nเกิดข้อผิดพลาด: {error}")


if __name__ == "__main__":
    main()
