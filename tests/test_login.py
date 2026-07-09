import os

from playwright.sync_api import expect

from pageObjects.login_page import LoginPage

ORANGEHRM_URL = os.getenv("ORANGEHRM_URL", "https://opensource-demo.orangehrmlive.com")
ORANGEHRM_USER = os.getenv("ORANGEHRM_USER", "Admin")
ORANGEHRM_PASS = os.getenv("ORANGEHRM_PASS", "admin123")


def test_valid_login_reaches_dashboard(fresh_page, logger):
    assert False, "Deliberate failure to demo Grafana failure visibility - reverted next commit"
    login_page = LoginPage(fresh_page, ORANGEHRM_URL)
    login_page.login(ORANGEHRM_USER, ORANGEHRM_PASS)

    expect(fresh_page).to_have_url(f"{ORANGEHRM_URL}/web/index.php/dashboard/index", timeout=20000)
    logger.info("Valid login reached the dashboard")


def test_wrong_password_shows_invalid_credentials(fresh_page):
    login_page = LoginPage(fresh_page, ORANGEHRM_URL)
    login_page.login(ORANGEHRM_USER, "not-the-real-password")

    expect(login_page.get_error_alert()).to_have_text("Invalid credentials", timeout=10000)


def test_wrong_username_shows_invalid_credentials(fresh_page):
    login_page = LoginPage(fresh_page, ORANGEHRM_URL)
    login_page.login("NotARealUser", ORANGEHRM_PASS)

    expect(login_page.get_error_alert()).to_have_text("Invalid credentials", timeout=10000)


def test_empty_fields_show_required_validation(fresh_page):
    login_page = LoginPage(fresh_page, ORANGEHRM_URL)
    login_page.goto()
    login_page.click_login()

    errors = login_page.get_field_errors()
    expect(errors).to_have_count(2, timeout=10000)
    expect(errors.first).to_have_text("Required")


def test_empty_username_only_shows_single_required_error(fresh_page):
    login_page = LoginPage(fresh_page, ORANGEHRM_URL)
    login_page.goto()
    login_page.fill_password(ORANGEHRM_PASS)
    login_page.click_login()

    errors = login_page.get_field_errors()
    expect(errors).to_have_count(1, timeout=10000)
