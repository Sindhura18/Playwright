
import pytest
from playwright.sync_api import sync_playwright
def test_playwright_python_heading(page):
    """Verify the main heading text on Playwright Python page"""
    page.goto("https://playwright.dev/python", timeout=60000)
    page.wait_for_load_state("networkidle")
    heading_text = page.inner_text("h1")
    assert "Playwright enables reliable end-to-end testing for modern web apps." in heading_text

