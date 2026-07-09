from utils.locators import Inputs, CommonLocators, EmployeeListLocators


class EmployeeListPage:
    """PIM > Employee List: search, CRUD, and the Personal Details/detail view."""

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto(self):
        self.page.goto(self.base_url + Inputs.PIM_EMPLOYEE_LIST_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)
        self.page.wait_for_selector(CommonLocators.TABLE_ROW, timeout=Inputs.LONG_TIMEOUT)

    def goto_add_employee(self):
        self.page.goto(self.base_url + Inputs.PIM_ADD_EMPLOYEE_PATH, wait_until="domcontentloaded")
        self.page.wait_for_selector(CommonLocators.FORM, timeout=Inputs.LONG_TIMEOUT)

    def _input_groups(self):
        return self.page.locator(CommonLocators.INPUT_GROUP)

    def fill_search_employee_name(self, name):
        group = self._input_groups().nth(EmployeeListLocators.EMPLOYEE_NAME_FIELD_INDEX)
        auto_input = group.locator(CommonLocators.GENERIC_INPUT)
        auto_input.click()
        auto_input.type(name, delay=30)
        self.page.wait_for_selector(CommonLocators.AUTOCOMPLETE_OPTION, timeout=Inputs.DEFAULT_TIMEOUT)
        self.page.wait_for_function(
            "document.querySelector('.oxd-autocomplete-option') "
            "&& !document.querySelector('.oxd-autocomplete-option').textContent.includes('Searching')"
        )

    def fill_search_employee_id(self, employee_id):
        group = self._input_groups().nth(EmployeeListLocators.EMPLOYEE_ID_FIELD_INDEX)
        group.locator(CommonLocators.GENERIC_INPUT).fill(employee_id)

    def select_search_employment_status(self, status_text):
        group = self._input_groups().nth(EmployeeListLocators.EMPLOYMENT_STATUS_FIELD_INDEX)
        group.locator(CommonLocators.SELECT_TEXT).click()
        self.page.locator(CommonLocators.SELECT_OPTION).get_by_text(status_text, exact=True).click()

    def get_autocomplete_options(self):
        return self.page.locator(CommonLocators.AUTOCOMPLETE_OPTION)

    def click_search(self):
        self.page.get_by_role("button", name=EmployeeListLocators.SEARCH_BUTTON_TEXT).click()

    def click_reset(self):
        self.page.get_by_role("button", name=EmployeeListLocators.RESET_BUTTON_TEXT).click()

    def click_add(self):
        self.page.get_by_role("button", name=EmployeeListLocators.ADD_BUTTON_TEXT, exact=True).click()

    def get_table_rows(self):
        return self.page.locator(CommonLocators.TABLE_ROW)

    def get_no_records_text(self):
        return self.page.locator(CommonLocators.NO_RECORDS_TEXT).first

    def select_row_checkbox(self, row_index):
        self.get_table_rows().nth(row_index).locator(CommonLocators.ROW_CHECKBOX_ICON).click(force=True)

    def click_delete_selected(self):
        self.page.get_by_role("button", name=EmployeeListLocators.DELETE_SELECTED_BUTTON_TEXT).click()

    def click_row_delete(self, row_index):
        self.get_table_rows().nth(row_index).locator(CommonLocators.ROW_ACTION_DELETE).click()

    def confirm_delete(self):
        self.page.get_by_role("button", name=EmployeeListLocators.CONFIRM_YES_DELETE_TEXT).click()

    def get_toast(self):
        return self.page.locator(CommonLocators.TOAST)

    def click_employee_link(self, name_text):
        self.page.get_by_role("link", name=name_text).first.click()

    # --- Add Employee form ---
    def fill_first_name(self, first_name):
        self.page.locator(CommonLocators.GENERIC_OXD_INPUT).nth(EmployeeListLocators.FIRST_NAME_INPUT_INDEX).fill(first_name)

    def fill_middle_name(self, middle_name):
        self.page.locator(CommonLocators.GENERIC_OXD_INPUT).nth(EmployeeListLocators.MIDDLE_NAME_INPUT_INDEX).fill(middle_name)

    def fill_last_name(self, last_name):
        self.page.locator(CommonLocators.GENERIC_OXD_INPUT).nth(EmployeeListLocators.LAST_NAME_INPUT_INDEX).fill(last_name)

    def click_save(self):
        self.page.get_by_role("button", name=EmployeeListLocators.SAVE_BUTTON_TEXT).click()

    def click_save_personal_details(self):
        """Clicks the first of the Personal Details page's two independent Save
        buttons (top identity/ID section vs. the lower Blood Type/custom-fields
        section) - this one covers the Employee Id field."""
        self.page.get_by_role("button", name=EmployeeListLocators.SAVE_BUTTON_TEXT).first.click()

    def wait_for_personal_details_page(self):
        """Waits for navigation to Personal Details and for its data (first name)
        to finish an async fetch. Polls window.location directly rather than using
        wait_for_url(), since this Vue-router SPA's pushState routing doesn't
        reliably fire the navigation events wait_for_url() listens for."""
        self.page.wait_for_function(
            "window.location.href.includes('viewPersonalDetails')",
            timeout=Inputs.LONG_TIMEOUT,
        )
        self.page.wait_for_function(
            "() => { const el = document.querySelector(\"input[name='firstName']\"); "
            "return !!el && el.value !== ''; }",
            timeout=Inputs.LONG_TIMEOUT,
        )

    def get_field_errors(self):
        return self.page.locator(CommonLocators.FIELD_ERROR_MESSAGE)

    # --- Detail view ---
    def click_detail_tab(self, tab_name):
        self.page.get_by_role("link", name=tab_name, exact=True).click()

    def get_employee_full_name_value(self):
        first = self.page.locator(EmployeeListLocators.FIRST_NAME_INPUT).input_value()
        last = self.page.locator(EmployeeListLocators.LAST_NAME_INPUT).input_value()
        return f"{first} {last}"

    def get_employee_id_value(self):
        group = self._input_groups().nth(EmployeeListLocators.EMPLOYEE_ID_INPUT_INDEX)
        return group.locator(CommonLocators.GENERIC_INPUT).input_value()

    def fill_employee_id(self, employee_id):
        group = self._input_groups().nth(EmployeeListLocators.EMPLOYEE_ID_INPUT_INDEX)
        field = group.locator(CommonLocators.GENERIC_INPUT)
        field.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Delete")
        field.type(employee_id, delay=20)

    def get_page_heading(self):
        return self.page.locator(EmployeeListLocators.PAGE_HEADING)

    def get_current_url(self):
        return self.page.url
