
import os
import pytest
from playwright.sync_api import sync_playwright

# Ensure screenshots directory exists
def ensure_screenshot_dir():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()

# Hook to capture screenshot and attach to HTML report on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            ensure_screenshot_dir()
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            # Attach screenshot to HTML report
            if hasattr(report, "extra"):
                report.extra.append(pytest.html.extras.image(screenshot_path))
