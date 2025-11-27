
import pytest
from playwright.sync_api import sync_playwright


def test_w3schools_heading(page):
    """Verify the main heading text on W3Schools homepage"""
    page.goto("https://www.w3schools.com", timeout=60000)
    page.wait_for_load_state("networkidle")
    heading_text = page.inner_text("h1")
    assert "Learn to Code" in heading_text
