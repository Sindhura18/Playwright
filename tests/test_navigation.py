import pytest
from playwright.sync_api import sync_playwright


def test_example_navigation(page):
    """Click the link and verify navigation to iana.org"""
    page.goto("https://example.com", timeout=6000)
    page.wait_for_load_state("networkidle")
    page.click("a")  # Click the link
    assert "iana.org" in page.url

