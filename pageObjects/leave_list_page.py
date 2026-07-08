from utils.helpers import set_date_field
from utils.locators import Inputs, CommonLocators, LeaveListLocators


class LeaveListPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto_apply(self):
        self.page.goto(self.base_url + Inputs.LEAVE_APPLY_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)

    def goto_assign(self):
        self.page.goto(self.base_url + Inputs.LEAVE_ASSIGN_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)

    def goto_list(self):
        self.page.goto(self.base_url + Inputs.LEAVE_LIST_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)

    # --- Apply / Assign leave ---
    def fill_employee_name(self, name):
        auto_input = self.page.locator(CommonLocators.AUTOCOMPLETE_INPUT).first
        auto_input.click()
        auto_input.type(name, delay=30)
        self.page.wait_for_selector(CommonLocators.AUTOCOMPLETE_OPTION, timeout=Inputs.DEFAULT_TIMEOUT)
        self.page.wait_for_function(
            "document.querySelector('.oxd-autocomplete-option') "
            "&& !document.querySelector('.oxd-autocomplete-option').textContent.includes('Searching')"
        )

    def get_autocomplete_options(self):
        return self.page.locator(CommonLocators.AUTOCOMPLETE_OPTION)

    def select_leave_type(self, option_index=1):
        self.page.locator(CommonLocators.SELECT_TEXT).first.click()
        self.page.locator(CommonLocators.SELECT_OPTION).nth(option_index).click()

    def fill_from_date(self, value):
        date_input = self.page.locator(LeaveListLocators.DATE_INPUT).nth(0)
        set_date_field(self.page, date_input, value)

    def fill_to_date(self, value):
        date_input = self.page.locator(LeaveListLocators.DATE_INPUT).nth(1)
        set_date_field(self.page, date_input, value)

    def fill_comment(self, comment):
        self.page.locator(LeaveListLocators.COMMENT_TEXTAREA).fill(comment)

    def click_apply(self):
        self.page.get_by_role("button", name=LeaveListLocators.APPLY_BUTTON_TEXT).click()

    def click_assign(self):
        self.page.get_by_role("button", name=LeaveListLocators.ASSIGN_BUTTON_TEXT).click()

    def get_ok_button(self):
        return self.page.get_by_role("button", name=LeaveListLocators.OK_BUTTON_TEXT)

    def click_ok_confirm(self):
        self.get_ok_button().click()

    def get_toast(self):
        return self.page.locator(CommonLocators.TOAST)

    # --- Leave list filter ---
    def select_status_filter(self, status_text):
        group = self.page.locator(CommonLocators.INPUT_GROUP).nth(LeaveListLocators.STATUS_SELECT_INDEX)
        group.locator(CommonLocators.SELECT_TEXT).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(status_text, exact=True).click()

    def fill_filter_employee_name(self, name):
        self.fill_employee_name(name)
        self.get_autocomplete_options().first.click()

    def click_search(self):
        self.page.get_by_role("button", name="Search").click()

    def click_reset(self):
        self.page.get_by_role("button", name="Reset").click()

    def get_table_rows(self):
        return self.page.locator(CommonLocators.TABLE_ROW)

    def click_row_approve(self, row_index):
        self.get_table_rows().nth(row_index).get_by_role("button", name=LeaveListLocators.APPROVE_BUTTON_TEXT).click()

    def click_row_reject(self, row_index):
        self.get_table_rows().nth(row_index).get_by_role("button", name=LeaveListLocators.REJECT_BUTTON_TEXT).click()

    def get_row_status_text(self, row_index):
        cells = self.get_table_rows().nth(row_index).locator(CommonLocators.TABLE_CELL)
        return cells.nth(LeaveListLocators.STATUS_TEXT_CELL_INDEX).text_content()
