from playwright.sync_api import expect

from utils.helpers import unique_suffix


def _add_throwaway_user(pages, username):
    # A broad single-letter query is used (rather than a fixed name) because this
    # autocomplete only offers employees who don't already have a system user account,
    # and repeated runs against the shared public demo steadily use up any one fixed name.
    pages.user_management.goto_add_user()
    pages.user_management.select_add_user_role("ESS")
    pages.user_management.fill_add_employee_name("e")
    pages.user_management.select_add_status("Enabled")
    pages.user_management.fill_add_username(username)
    pages.user_management.fill_add_password("Test@12345")
    pages.user_management.fill_add_confirm_password("Test@12345")
    pages.user_management.click_save()
    expect(pages.user_management.get_toast()).to_contain_text("Successfully Saved", timeout=10000)


def _search_username(pages, username):
    pages.user_management.goto()
    pages.user_management.fill_search_username(username)
    pages.user_management.click_search()
    pages.user_management.page.wait_for_timeout(1500)


def test_bulk_delete_bar_hidden_until_row_selected(pages):
    # Row 0 of an unfiltered list can be the currently logged-in Admin account itself,
    # which OrangeHRM silently refuses to add to a bulk selection (self-protection), so
    # this uses a throwaway user we just created to guarantee a selectable row.
    username = f"zqauto_{unique_suffix()}"
    _add_throwaway_user(pages, username)
    _search_username(pages, username)
    pages.user_management.get_table_rows().first.wait_for(timeout=10000)

    expect(pages.user_management.get_bulk_action_bar_text()).to_have_count(0)
    pages.user_management.select_row_checkbox(0)
    expect(pages.user_management.get_bulk_action_bar_text()).to_be_visible(timeout=10000)

    # cleanup so this throwaway user doesn't linger on the shared demo
    pages.user_management.click_delete_selected()
    pages.user_management.confirm_delete()


def test_bulk_delete_single_selected_user(pages):
    username = f"zqauto_{unique_suffix()}"
    _add_throwaway_user(pages, username)

    _search_username(pages, username)
    pages.user_management.get_table_rows().first.wait_for(timeout=10000)
    pages.user_management.select_row_checkbox(0)
    pages.user_management.click_delete_selected()
    pages.user_management.confirm_delete()
    expect(pages.user_management.get_toast()).to_contain_text("Successfully Deleted", timeout=10000)

    _search_username(pages, username)
    expect(pages.user_management.get_no_records_text()).to_be_visible(timeout=10000)


def test_bulk_delete_multiple_selected_users(pages):
    # Row 0 of the unfiltered list can be the currently logged-in Admin account, which
    # OrangeHRM refuses to include in a bulk selection, so rows 1 and 2 are used instead
    # to exercise genuine multi-row bulk selection in a single action.
    pages.user_management.goto()
    rows = pages.user_management.get_table_rows()
    username_1 = rows.nth(1).locator(".oxd-table-cell").nth(1).text_content().strip()
    username_2 = rows.nth(2).locator(".oxd-table-cell").nth(1).text_content().strip()

    pages.user_management.select_row_checkbox(1)
    pages.user_management.select_row_checkbox(2)
    pages.user_management.click_delete_selected()
    pages.user_management.confirm_delete()
    expect(pages.user_management.get_toast()).to_contain_text("Successfully Deleted", timeout=10000)

    for username in (username_1, username_2):
        _search_username(pages, username)
        expect(pages.user_management.get_no_records_text()).to_be_visible(timeout=10000)


def test_cancel_delete_leaves_user_intact(pages):
    username = f"zqauto_{unique_suffix()}"
    _add_throwaway_user(pages, username)

    _search_username(pages, username)
    pages.user_management.get_table_rows().first.wait_for(timeout=10000)
    pages.user_management.select_row_checkbox(0)
    pages.user_management.click_delete_selected()
    pages.user_management.cancel_delete()

    _search_username(pages, username)
    expect(pages.user_management.get_table_rows()).to_have_count(1, timeout=10000)

    # cleanup so this throwaway user doesn't linger on the shared demo
    pages.user_management.select_row_checkbox(0)
    pages.user_management.click_delete_selected()
    pages.user_management.confirm_delete()


def test_deleted_user_not_findable_by_role_filter(pages):
    username = f"zqauto_{unique_suffix()}"
    _add_throwaway_user(pages, username)

    _search_username(pages, username)
    pages.user_management.get_table_rows().first.wait_for(timeout=10000)
    pages.user_management.select_row_checkbox(0)
    pages.user_management.click_delete_selected()
    pages.user_management.confirm_delete()
    expect(pages.user_management.get_toast()).to_contain_text("Successfully Deleted", timeout=10000)

    pages.user_management.goto()
    pages.user_management.fill_search_username(username)
    pages.user_management.select_search_user_role("ESS")
    pages.user_management.click_search()
    expect(pages.user_management.get_no_records_text()).to_be_visible(timeout=10000)
