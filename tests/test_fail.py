import pytest
from playwright.sync_api import sync_playwright

def test_fail_example(page):
    """This test will fail intentionally by checking wrong heading text"""
    page.goto("https://example.com", timeout=6000)
    page.wait_for_load_state("networkidle")
    # Intentionally wrong assertion
    assert page.inner_text("h1") == "This Will Fail"
