from utils.locators import Inputs, LoginLocators


class LoginPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto(self):
        self.page.goto(self.base_url + Inputs.ORANGEHRM_LOGIN_PATH, wait_until="domcontentloaded")

    def fill_username(self, username):
        self.page.locator(LoginLocators.USERNAME_INPUT).fill(username)

    def fill_password(self, password):
        self.page.locator(LoginLocators.PASSWORD_INPUT).fill(password)

    def click_login(self):
        self.page.locator(LoginLocators.LOGIN_BUTTON).click()

    def login(self, username, password):
        self.goto()
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_login_button(self):
        return self.page.locator(LoginLocators.LOGIN_BUTTON)

    def get_error_alert(self):
        return self.page.locator(LoginLocators.ERROR_ALERT)

    def get_field_errors(self):
        return self.page.locator("css=.oxd-input-field-error-message")

    def get_username_value(self):
        return self.page.locator(LoginLocators.USERNAME_INPUT).input_value()
