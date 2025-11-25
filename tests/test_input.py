import pytest
from playwright.sync_api import sync_playwright

def test_form_submission():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.w3schools.com/html/html_forms.asp", timeout=6000)
        page.fill('input[name="firstname"]', "John")
        page.fill('input[name="lastname"]', "Doe")
        page.click('input[type="submit"]')
        # Validate navigation or response
        assert "html" in page.url
