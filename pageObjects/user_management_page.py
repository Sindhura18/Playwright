from utils.locators import Inputs, CommonLocators, UserManagementLocators


class UserManagementPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto(self):
        self.page.goto(self.base_url + Inputs.ADMIN_USERS_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)
        self.page.wait_for_selector(CommonLocators.TABLE_ROW, timeout=Inputs.LONG_TIMEOUT)

    def goto_add_user(self):
        self.page.goto(self.base_url + Inputs.ADMIN_ADD_USER_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)

    def _input_groups(self):
        return self.page.locator(CommonLocators.INPUT_GROUP)

    def fill_search_username(self, username):
        self._input_groups().nth(UserManagementLocators.USERNAME_FIELD_INDEX).locator("input").fill(username)

    def select_search_user_role(self, role_text):
        group = self._input_groups().nth(UserManagementLocators.USER_ROLE_FIELD_INDEX)
        group.locator(CommonLocators.SELECT_TEXT).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(role_text, exact=True).click()

    def select_search_status(self, status_text):
        group = self._input_groups().nth(UserManagementLocators.STATUS_FIELD_INDEX)
        group.locator(CommonLocators.SELECT_TEXT).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(status_text, exact=True).click()

    def click_search(self):
        self.page.get_by_role("button", name="Search").click()

    def click_reset(self):
        self.page.get_by_role("button", name="Reset").click()

    def click_add(self):
        self.page.get_by_role("button", name=UserManagementLocators.ADD_BUTTON_TEXT, exact=True).click()

    def get_table_rows(self):
        return self.page.locator(CommonLocators.TABLE_ROW)

    def get_no_records_text(self):
        return self.page.locator(CommonLocators.NO_RECORDS_TEXT).first

    def select_row_checkbox(self, row_index):
        self.get_table_rows().nth(row_index).locator(CommonLocators.ROW_CHECKBOX_ICON).click(force=True)

    def click_delete_selected(self):
        self.page.get_by_role("button", name=UserManagementLocators.DELETE_SELECTED_BUTTON_TEXT).click()

    def click_row_delete(self, row_index):
        self.get_table_rows().nth(row_index).locator(CommonLocators.ROW_ACTION_DELETE).click()

    def confirm_delete(self):
        self.page.get_by_role("button", name=UserManagementLocators.CONFIRM_YES_DELETE_TEXT).click()

    def cancel_delete(self):
        self.page.get_by_role("button", name=UserManagementLocators.CONFIRM_NO_CANCEL_TEXT).click()

    def get_toast(self):
        return self.page.locator(CommonLocators.TOAST)

    def get_bulk_action_bar_text(self):
        return self.page.get_by_role("button", name=UserManagementLocators.DELETE_SELECTED_BUTTON_TEXT)

    # --- Add User form ---
    def select_add_user_role(self, role_text):
        self.page.locator(CommonLocators.SELECT_TEXT).nth(UserManagementLocators.ADD_USER_ROLE_INDEX).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(role_text, exact=True).click()

    def fill_add_employee_name(self, name):
        auto_input = self.page.locator(CommonLocators.AUTOCOMPLETE_INPUT).first
        auto_input.type(name, delay=30)
        self.page.wait_for_selector(CommonLocators.AUTOCOMPLETE_OPTION, timeout=Inputs.DEFAULT_TIMEOUT)
        self.page.wait_for_function(
            "document.querySelector('.oxd-autocomplete-option') "
            "&& !document.querySelector('.oxd-autocomplete-option').textContent.includes('Searching')"
        )
        self.page.locator(CommonLocators.AUTOCOMPLETE_OPTION).first.click()

    def select_add_status(self, status_text):
        self.page.locator(CommonLocators.SELECT_TEXT).nth(UserManagementLocators.ADD_STATUS_INDEX).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(status_text, exact=True).click()

    def fill_add_username(self, username):
        self.page.locator("input.oxd-input").nth(1).fill(username)

    def fill_add_password(self, password):
        self.page.locator("input.oxd-input").nth(2).fill(password)

    def fill_add_confirm_password(self, password):
        self.page.locator("input.oxd-input").nth(3).fill(password)

    def click_save(self):
        self.page.get_by_role("button", name=UserManagementLocators.SAVE_BUTTON_TEXT).click()

    def get_field_errors(self):
        return self.page.locator(CommonLocators.FIELD_ERROR_MESSAGE)
