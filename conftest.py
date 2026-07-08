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

load_dotenv()

ORANGEHRM_URL = os.getenv("ORANGEHRM_URL", "https://opensource-demo.orangehrmlive.com")
ORANGEHRM_USER = os.getenv("ORANGEHRM_USER", "Admin")
ORANGEHRM_PASS = os.getenv("ORANGEHRM_PASS", "admin123")
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"


def _ensure_screenshot_dir():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")


@pytest.fixture(scope="session")
def logger():
    log = logging.getLogger("orangehrm_suite")
    if not log.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        log.addHandler(handler)
        log.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    return log


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
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
    login_page = LoginPage(page, ORANGEHRM_URL)
    login_page.login(ORANGEHRM_USER, ORANGEHRM_PASS)
    page.wait_for_selector("h6.oxd-text--h6", timeout=30000)
    logger.info("Logged into OrangeHRM as %s", ORANGEHRM_USER)
    yield page
    context.close()


@dataclass
class OrangeHRMPages:
    login: LoginPage
    user_management: UserManagementPage
    employee_list: EmployeeListPage
    leave_list: LeaveListPage


@pytest.fixture(scope="module")
def pages(orangehrm_login):
    page = orangehrm_login
    return OrangeHRMPages(
        login=LoginPage(page, ORANGEHRM_URL),
        user_management=UserManagementPage(page, ORANGEHRM_URL),
        employee_list=EmployeeListPage(page, ORANGEHRM_URL),
        leave_list=LeaveListPage(page, ORANGEHRM_URL),
    )


@pytest.fixture(scope="module")
def mailinator_page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = None
        for fixture_name in ("orangehrm_login", "fresh_page", "mailinator_page"):
            candidate = item.funcargs.get(fixture_name)
            if candidate is not None:
                page = candidate
                break
        if page:
            _ensure_screenshot_dir()
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            if hasattr(report, "extra"):
                report.extra.append(pytest.html.extras.image(screenshot_path))
