# OKLV AI Factory — Web

เว็บแอปเวอร์ชันของ OKLV AI Factory ใช้ AI สองตัวต่อกัน (Gemini) วางแผน
แคมเปญโฆษณาสั้น 30 วินาที 4 ฉาก แล้วสร้าง image/video prompt สำหรับแต่ละฉาก
เปิดใช้งานได้จากเบราว์เซอร์บนมือถือ, iPad, หรือคอมพิวเตอร์เครื่องไหนก็ได้
ไม่ต้องติดตั้ง Python บนอุปกรณ์ที่ใช้งาน

## รันในเครื่องตัวเอง

```bash
pip install -r requirements.txt
cp .env.example .env   # แล้วใส่ GEMINI_API_KEY จริงลงไป
python app.py
```

เปิด `http://localhost:5000`

## Deploy ขึ้น Render (ฟรี)

1. Push โค้ดนี้ขึ้น GitHub repo (ไฟล์นี้ไม่รวม `.env` แล้ว เพราะอยู่ใน
   `.gitignore` — ห้ามใส่ API key ลงในโค้ดที่ push ขึ้น GitHub เด็ดขาด)
2. ไปที่ [render.com](https://render.com) → New → Web Service → เลือก
   repo นี้
3. ตั้งค่า:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. ไปที่แท็บ **Environment** → เพิ่มตัวแปร:
   - `GEMINI_API_KEY` = key จริงของคุณ
   - `GEMINI_MODEL` = `gemini-3.6-flash` (หรือรุ่นที่ใช้อยู่)
5. Deploy — Render จะให้ URL แบบ `https://your-app.onrender.com` มาใช้
   เปิดจากมือถือ/iPad ได้ทันที

ทุกครั้งที่ push โค้ดใหม่ขึ้น GitHub, Render จะ build และ deploy ให้อัตโนมัติ

## โครงสร้างไฟล์

- `app.py` — Flask app, route หน้าแรกและ `/generate`
- `planner.py` / `prompt_engine.py` / `models.py` — ตรรกะ AI เดิม (ไม่แก้)
- `templates/index.html` — หน้าเว็บ (ฟอร์ม + ผลลัพธ์)
- `static/style.css` — สไตล์
- `Procfile` — บอก Render ว่าจะรันแอปด้วยคำสั่งอะไร
