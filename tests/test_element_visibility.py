import pytest
from playwright.sync_api import sync_playwright

def test_example_text():
    """Verify the main heading text on example.com"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com",timeout=6000)
        page.wait_for_load_state("networkidle")
        assert page.inner_text("h1") == "Example Domain"
        browser.close()

