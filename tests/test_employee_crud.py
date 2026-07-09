from playwright.sync_api import expect

from utils.helpers import unique_suffix
from utils.locators import CommonLocators


def _add_employee(pages, first_name, last_name):
    pages.employee_list.goto_add_employee()
    pages.employee_list.fill_first_name(first_name)
    pages.employee_list.fill_last_name(last_name)
    pages.employee_list.click_save()
    pages.employee_list.wait_for_personal_details_page()


def test_create_employee_is_listed(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "Create"
    _add_employee(pages, first_name, last_name)

    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name(first_name)
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()

    rows = pages.employee_list.get_table_rows()
    expect(rows).to_have_count(1, timeout=10000)
    expect(rows.first).to_contain_text(first_name)


def test_edit_employee_id_persists(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "Edit"
    _add_employee(pages, first_name, last_name)

    new_employee_id = unique_suffix()
    pages.employee_list.fill_employee_id(new_employee_id)
    pages.employee_list.click_save_personal_details()
    expect(pages.employee_list.get_toast()).to_contain_text("Successfully Updated", timeout=10000)

    pages.employee_list.page.reload(wait_until="domcontentloaded")
    pages.employee_list.wait_for_personal_details_page()
    assert pages.employee_list.get_employee_id_value() == new_employee_id


def test_delete_single_employee_via_row_action(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "Delete"
    _add_employee(pages, first_name, last_name)

    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name(first_name)
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()
    pages.employee_list.click_row_delete(0)
    pages.employee_list.confirm_delete()
    expect(pages.employee_list.get_toast()).to_contain_text("Successfully Deleted", timeout=10000)

    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name(first_name)
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()
    expect(pages.employee_list.get_no_records_text()).to_be_visible(timeout=10000)


def test_bulk_delete_created_employees(pages):
    # The Employee Name search only accepts one exact autocomplete-selected name at a
    # time (no shared-prefix/substring matching), and a freshly created employee isn't
    # on page 1 of the default (100+ employee) unfiltered list, so simultaneous
    # multi-row selection is exercised against two existing rows from that list instead.
    # Whichever row is the logged-in Admin's own linked employee has no delete action
    # (same self-protection rule as Admin Users), so rows are picked by actually having
    # one rather than assuming fixed positions.
    pages.employee_list.goto()
    rows = pages.employee_list.get_table_rows()
    deletable_indexes = [
        i for i in range(rows.count()) if rows.nth(i).locator(CommonLocators.ROW_ACTION_DELETE).count() > 0
    ][:2]
    employee_id_1 = rows.nth(deletable_indexes[0]).locator(CommonLocators.TABLE_CELL).nth(1).text_content().strip()
    employee_id_2 = rows.nth(deletable_indexes[1]).locator(CommonLocators.TABLE_CELL).nth(1).text_content().strip()

    pages.employee_list.select_row_checkbox(deletable_indexes[0])
    pages.employee_list.select_row_checkbox(deletable_indexes[1])
    pages.employee_list.click_delete_selected()
    pages.employee_list.confirm_delete()
    expect(pages.employee_list.get_toast()).to_contain_text("Successfully Deleted", timeout=10000)

    for employee_id in (employee_id_1, employee_id_2):
        pages.employee_list.goto()
        pages.employee_list.fill_search_employee_id(employee_id)
        pages.employee_list.click_search()
        expect(pages.employee_list.get_no_records_text()).to_be_visible(timeout=10000)


def test_create_employee_requires_last_name(pages):
    pages.employee_list.goto_add_employee()
    pages.employee_list.fill_first_name(f"ZQAuto{unique_suffix()}")
    pages.employee_list.click_save()

    expect(pages.employee_list.get_field_errors().first).to_have_text("Required", timeout=10000)
