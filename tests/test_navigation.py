import pytest
from playwright.sync_api import sync_playwright

def test_example_navigation():
    """Click the link and verify navigation to iana.org"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com", timeout=6000)
        page.click("a")  # Click the link
        assert "iana.org" in page.url
        browser.close()

