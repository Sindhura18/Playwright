import logging
import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pageObjects.login_page import LoginPage
from pageObjects.user_management_page import UserManagementPage
from pageObjects.employee_list_page import EmployeeListPage
from pageObjects.leave_list_page import LeaveListPage
from utils.locators import LoginLocators

load_dotenv()

ORANGEHRM_URL = os.getenv("ORANGEHRM_URL", "https://opensource-demo.orangehrmlive.com")
ORANGEHRM_USER = os.getenv("ORANGEHRM_USER", "Admin")
ORANGEHRM_PASS = os.getenv("ORANGEHRM_PASS", "admin123")
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"


def _ensure_screenshot_dir():
    """Creates screenshots/ on first use (git-ignored, holds failure captures)."""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")


@pytest.fixture(scope="session")
def logger():
    """Console logger shared across the whole test session."""
    log = logging.getLogger("orangehrm_suite")
    if not log.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        log.addHandler(handler)
        log.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    return log


@pytest.fixture(scope="session")
def playwright_instance():
    """The sync_playwright driver, started once for the whole session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """One Chromium process for the whole session; individual test files get
    isolation via their own browser context, not a new browser process."""
    browser = playwright_instance.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def fresh_page(browser):
    """A brand-new context/page with no login - used by test_login.py so bad-credential
    scenarios never touch the shared logged-in session other test files use."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="module")
def orangehrm_login(browser, logger):
    """Logs in once per test module and hands back the authenticated page for every
    test in that file to reuse."""
    context = browser.new_context()
    page = context.new_page()
    try:
        login_page = LoginPage(page, ORANGEHRM_URL)
        login_page.login(ORANGEHRM_USER, ORANGEHRM_PASS)
        page.wait_for_selector(LoginLocators.DASHBOARD_LOADED_INDICATOR, timeout=30000)
    except Exception:
        _ensure_screenshot_dir()
        page.screenshot(path="screenshots/orangehrm_login_setup_failure.png")
        logger.error("orangehrm_login fixture failed to reach the dashboard", exc_info=True)
        context.close()
        raise
    logger.info("Logged into OrangeHRM as %s", ORANGEHRM_USER)
    yield page
    context.close()


@dataclass
class OrangeHRMPages:
    """Page objects bound to the one module-scoped authenticated page."""
    login: LoginPage
    user_management: UserManagementPage
    employee_list: EmployeeListPage
    leave_list: LeaveListPage


@pytest.fixture(scope="module")
def pages(orangehrm_login):
    """Bundles page objects for the shared authenticated page so tests don't
    re-instantiate them individually."""
    page = orangehrm_login
    return OrangeHRMPages(
        login=LoginPage(page, ORANGEHRM_URL),
        user_management=UserManagementPage(page, ORANGEHRM_URL),
        employee_list=EmployeeListPage(page, ORANGEHRM_URL),
        leave_list=LeaveListPage(page, ORANGEHRM_URL),
    )


@pytest.fixture(scope="module")
def mailinator_page(browser):
    """A fresh, unauthenticated context/page for the Mailinator test files."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attaches a screenshot of whichever page fixture a test used to the HTML
    report on failure, on both setup and call failures."""
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call") and report.failed:
        page = None
        for fixture_name in ("orangehrm_login", "fresh_page", "mailinator_page"):
            candidate = item.funcargs.get(fixture_name)
            if candidate is not None:
                page = candidate
                break
        if page:
            _ensure_screenshot_dir()
            screenshot_path = f"screenshots/{report.when}_{item.name}.png"
            page.screenshot(path=screenshot_path)
            if hasattr(report, "extra"):
                report.extra.append(pytest.html.extras.image(screenshot_path))
