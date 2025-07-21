from flask import Flask
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live. Use /run to trigger it."

@app.route('/run')
def run_bot():
    email = os.getenv("FNL_EMAIL")
    password = os.getenv("FNL_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login
        page.goto("https://fnlb.net/login")
        page.fill('input[type="email"]', email)
        page.fill('input[type="password"]', password)
        page.click('button:has-text("Log in")')
        page.wait_for_url("https://app.fnlb.net/*", timeout=15000)

        # Go to bot page
        page.goto("https://app.fnlb.net/bot/67fad93a739ee0f4991bb53c")
        page.wait_for_timeout(5000)

        # Send command
        page.click('text=Chat')
        page.fill('textarea[placeholder="Run a command..."]', "floss")
        page.click('button:has-text("Send")')

        browser.close()

    return "Command sent: floss"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
