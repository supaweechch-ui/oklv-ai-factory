"""Flask web front end for OKLV AI Factory.

Wraps the existing two-agent pipeline (planner.create_campaign +
prompt_engine.create_visual_prompts) behind a simple form so it can run
anywhere with a browser instead of only inside a Windows terminal.
"""

import os

from flask import Flask, render_template, request
from google.genai.errors import APIError
from httpx import RequestError
from pydantic import ValidationError

from planner import create_campaign
from prompt_engine import create_visual_prompts

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", campaign=None, prompts=None,
        production_notes=None, error=None, form={},
    )


@app.route("/generate", methods=["POST"])
def generate():
    form = {
        "product": request.form.get("product", "").strip(),
        "target": request.form.get("target", "").strip(),
        "selling_point": request.form.get("selling_point", "").strip(),
    }

    if not all(form.values()):
        return render_template(
            "index.html", campaign=None, prompts=None,
            production_notes=None,
            error="กรอกข้อมูลให้ครบทั้งสามช่องก่อนสร้างแคมเปญ",
            form=form,
        )

    try:
        campaign = create_campaign(
            form["product"], form["target"], form["selling_point"]
        )
        visual_prompts = create_visual_prompts(campaign)
        return render_template(
            "index.html",
            campaign=campaign,
            prompts=visual_prompts.prompts,
            production_notes=visual_prompts.production_notes,
            error=None,
            form=form,
        )
    except APIError as error:
        message = (
            "เชื่อมต่อ Gemini API ไม่สำเร็จ — ตรวจสอบว่า GEMINI_API_KEY "
            f"ถูกต้องและยังใช้งานได้ ({error})"
        )
    except RequestError:
        message = (
            "เชื่อมต่อ Gemini API ไม่ได้ — ตรวจสอบอินเทอร์เน็ต, DNS, VPN "
            "หรือ firewall แล้วลองใหม่อีกครั้ง"
        )
    except (RuntimeError, ValueError, ValidationError) as error:
    message = f"เกิดข้อผิดพลาด: {error}"
    except Exception as error:
    message = f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {error}"

    return render_template(
        "index.html", campaign=None, prompts=None,
        production_notes=None, error=message, form=form,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
