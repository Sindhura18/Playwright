
import pytest
from playwright.sync_api import sync_playwright

def test_playwright_python_heading():
    """Verify the main heading text on Playwright Python page"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://playwright.dev/python", timeout=60000)
        page.wait_for_load_state("networkidle")
        # Check the main heading text
        heading_text = page.inner_text("h1")
        assert "Playwright enables reliable end-to-end testing for modern web apps." in heading_text
        browser.close()
