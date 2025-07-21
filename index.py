from playwright.sync_api import sync_playwright
import time
import os

EMAIL = os.getenv("FNL_EMAIL")  # set this on Render as environment variable
PASSWORD = os.getenv("FNL_PASSWORD")

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Go to login page
        page.goto("https://fnlb.net/login")

        # 2. Fill in login
        page.fill('input[type="email"]', EMAIL)
        page.fill('input[type="password"]', PASSWORD)
        page.click('button:has-text("Log in")')

        # 3. Wait for navigation to dashboard
        page.wait_for_url("https://app.fnlb.net/*", timeout=15000)

        # 4. Navigate to bot page
        page.goto("https://app.fnlb.net/bot/67fad93a739ee0f4991bb53c")
        page.wait_for_timeout(5000)

        # 5. Open chat (should already be visible)
        page.click('text=Chat')

        # 6. Type "floss"
        page.fill('textarea[placeholder="Run a command..."]', "floss")
        page.click('button:has-text("Send")')

        # 7. Done
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    run_bot()
