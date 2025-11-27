import pytest
from playwright.sync_api import sync_playwright

def test_example_text(page):
    """Verify the main heading text on example.com"""
    page.goto("https://example.com", timeout=6000)
    page.wait_for_load_state("networkidle")
    assert page.inner_text("h1") == "Example Domain"
#hi

