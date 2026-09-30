import os
import time
import threading
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
from app import app, init_database

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

init_database()
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
time.sleep(2)

os.makedirs('screenshots', exist_ok=True)

def create_windows11_display(web_img: Image.Image, page_url: str, page_title: str) -> Image.Image:
    canvas_w, canvas_h = 1920, 1080
    top_bar_h = 82
    taskbar_h = 48
    viewport_h = canvas_h - top_bar_h - taskbar_h

    web_img_resized = web_img.resize((canvas_w, viewport_h), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (canvas_w, canvas_h), (240, 243, 246))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("segoeui.ttf", 13)
        font_url = ImageFont.truetype("segoeui.ttf", 13)
        font_clock = ImageFont.truetype("segoeui.ttf", 12)
        font_clock_bold = ImageFont.truetype("segoeuib.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_url = ImageFont.load_default()
        font_clock = ImageFont.load_default()
        font_clock_bold = ImageFont.load_default()

    # Chrome Top Bar
    draw.rectangle([0, 0, canvas_w, 40], fill=(222, 225, 230))
    draw.rounded_rectangle([80, 8, 340, 40], radius=8, fill=(255, 255, 255))
    draw.text((105, 16), page_title[:32], fill=(30, 30, 30), font=font_title)
    draw.text((320, 16), "×", fill=(100, 100, 100), font=font_title)

    draw.text((canvas_w - 120, 12), "─", fill=(80, 80, 80), font=font_title)
    draw.rectangle([canvas_w - 75, 14, canvas_w - 63, 26], outline=(80, 80, 80), width=1)
    draw.text((canvas_w - 30, 12), "✕", fill=(80, 80, 80), font=font_title)

    draw.rectangle([0, 40, canvas_w, top_bar_h], fill=(255, 255, 255))
    draw.line([0, top_bar_h-1, canvas_w, top_bar_h-1], fill=(218, 220, 224), width=1)

    draw.text((16, 52), "←", fill=(100, 100, 100), font=font_title)
    draw.text((46, 52), "→", fill=(160, 160, 160), font=font_title)
    draw.text((76, 52), "↻", fill=(80, 80, 80), font=font_title)

    draw.rounded_rectangle([110, 46, canvas_w - 120, 74], radius=14, fill=(241, 243, 244))
    draw.text((125, 52), "🔒", fill=(60, 60, 60), font=font_title)
    draw.text((150, 52), page_url, fill=(30, 30, 30), font=font_url)

    # Middle Web Content
    canvas.paste(web_img_resized, (0, top_bar_h))

    # Windows 11 Taskbar
    taskbar_y = canvas_h - taskbar_h
    draw.rectangle([0, taskbar_y, canvas_w, canvas_h], fill=(24, 28, 36))
    draw.line([0, taskbar_y, canvas_w, taskbar_y], fill=(45, 50, 60), width=1)

    center_x = canvas_w // 2
    start_x = center_x - 140
    draw.rectangle([start_x, taskbar_y + 14, start_x + 9, taskbar_y + 23], fill=(0, 164, 239))
    draw.rectangle([start_x + 11, taskbar_y + 14, start_x + 20, taskbar_y + 23], fill=(0, 164, 239))
    draw.rectangle([start_x, taskbar_y + 25, start_x + 9, taskbar_y + 34], fill=(0, 164, 239))
    draw.rectangle([start_x + 11, taskbar_y + 25, start_x + 20, taskbar_y + 34], fill=(0, 164, 239))

    draw.ellipse([start_x + 40, taskbar_y + 15, start_x + 55, taskbar_y + 30], outline=(200, 200, 200), width=2)
    icons = ["🗔", "📁", "🌐", "💻", "📝"]
    for idx, icon_text in enumerate(icons):
        ix = start_x + 80 + (idx * 40)
        if icon_text == "🌐":
            draw.rounded_rectangle([ix - 6, taskbar_y + 6, ix + 26, taskbar_y + 42], radius=4, fill=(45, 55, 72))
            draw.line([ix + 2, taskbar_y + 40, ix + 18, taskbar_y + 40], fill=(59, 130, 246), width=3)
        draw.text((ix, taskbar_y + 14), icon_text, fill=(220, 220, 220), font=font_title)

    # Taskbar Clock with Time & Date
    current_time_str = "06:28 AM"
    current_date_str = "30-09-2026"
    draw.text((canvas_w - 105, taskbar_y + 8), current_time_str, fill=(240, 240, 240), font=font_clock_bold)
    draw.text((canvas_w - 105, taskbar_y + 25), current_date_str, fill=(190, 195, 205), font=font_clock)
    draw.text((canvas_w - 175, taskbar_y + 15), "📶  🔊  🔋  ^", fill=(210, 215, 225), font=font_clock)

    return canvas

from io import BytesIO

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Capture Unauthenticated Pages
        unauth_context = browser.new_context(viewport={"width": 1920, "height": 952})
        page = unauth_context.new_page()

        unauth_pages = [
            ("screenshot_01_home.png", "http://127.0.0.1:5000/", "Diabetes Detection System - Home"),
            ("screenshot_02_login.png", "http://127.0.0.1:5000/login", "Diabetes Detection System - Login"),
            ("screenshot_03_signup.png", "http://127.0.0.1:5000/signup", "Diabetes Detection System - Sign Up"),
            ("screenshot_06_stats.png", "http://127.0.0.1:5000/stats", "Diabetes Detection System - Statistics"),
            ("screenshot_07_feedback.png", "http://127.0.0.1:5000/feedback", "Diabetes Detection System - Feedback"),
            ("screenshot_09_about.png", "http://127.0.0.1:5000/about", "Diabetes Detection System - About"),
            ("screenshot_10_contact.png", "http://127.0.0.1:5000/contact", "Diabetes Detection System - Contact"),
        ]

        for filename, url, title in unauth_pages:
            print(f"Capturing unauth {filename}...")
            page.goto(url)
            time.sleep(1)
            png_bytes = page.screenshot(full_page=False)
            web_img = Image.open(BytesIO(png_bytes))
            display_img = create_windows11_display(web_img, page.url, title)
            display_img.save(os.path.join("screenshots", filename))

        unauth_context.close()

        # 2. Capture Authenticated Pages
        auth_context = browser.new_context(viewport={"width": 1920, "height": 952})
        auth_page = auth_context.new_page()

        # Login
        auth_page.goto("http://127.0.0.1:5000/login")
        auth_page.fill("input[name='identifier']", "Jay Sitapara")
        auth_page.fill("input[name='password']", "admin123")
        auth_page.click("button[type='submit']")
        time.sleep(1)

        # Result page
        print("Capturing screenshot_04_result.png...")
        auth_page.goto("http://127.0.0.1:5000/predict")
        auth_page.fill("input[name='pregnancies']", "2")
        auth_page.fill("input[name='glucose']", "148")
        auth_page.fill("input[name='blood_pressure']", "72")
        auth_page.fill("input[name='skin_thickness']", "35")
        auth_page.fill("input[name='insulin']", "0")
        auth_page.fill("input[name='bmi']", "33.6")
        auth_page.fill("input[name='diabetes_pedigree']", "0.627")
        auth_page.fill("input[name='age']", "50")
        auth_page.click("button[type='submit']")
        time.sleep(1.5)
        png_bytes = auth_page.screenshot(full_page=False)
        web_img = Image.open(BytesIO(png_bytes))
        display_img = create_windows11_display(web_img, auth_page.url, "Diabetes Detection System - Assessment Result")
        display_img.save(os.path.join("screenshots", "screenshot_04_result.png"))

        # History page
        print("Capturing screenshot_05_history.png...")
        auth_page.goto("http://127.0.0.1:5000/history")
        time.sleep(1)
        png_bytes = auth_page.screenshot(full_page=False)
        web_img = Image.open(BytesIO(png_bytes))
        display_img = create_windows11_display(web_img, auth_page.url, "Diabetes Detection System - Prediction History")
        display_img.save(os.path.join("screenshots", "screenshot_05_history.png"))

        # Admin page
        print("Capturing screenshot_08_admin.png...")
        auth_page.goto("http://127.0.0.1:5000/admin")
        time.sleep(1)
        png_bytes = auth_page.screenshot(full_page=False)
        web_img = Image.open(BytesIO(png_bytes))
        display_img = create_windows11_display(web_img, auth_page.url, "Diabetes Detection System - Admin Dashboard")
        display_img.save(os.path.join("screenshots", "screenshot_08_admin.png"))

        auth_context.close()
        browser.close()

if __name__ == "__main__":
    capture_all()
