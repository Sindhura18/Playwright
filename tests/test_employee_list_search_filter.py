from playwright.sync_api import expect


def test_search_by_employee_name(pages):
    # A broad single-letter query is used rather than a fixed name because this
    # autocomplete only offers real (still-existing) employees, and repeated runs
    # against the shared public demo can delete any one fixed name over time.
    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name("e")
    selected_name = pages.employee_list.get_autocomplete_options().first.text_content().strip()
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()

    rows = pages.employee_list.get_table_rows()
    expect(rows.first).to_be_visible(timeout=10000)
    expect(rows.first).to_contain_text(selected_name.split()[0])


def test_search_by_employee_id(pages):
    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name("e")
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()
    employee_id = pages.employee_list.get_table_rows().first.locator(".oxd-table-cell").nth(1).text_content().strip()

    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_id(employee_id)
    pages.employee_list.click_search()

    rows = pages.employee_list.get_table_rows()
    expect(rows.first).to_be_visible(timeout=10000)
    expect(rows.first).to_contain_text(employee_id)


def test_filter_by_employment_status_does_not_error(pages):
    pages.employee_list.goto()
    pages.employee_list.select_search_employment_status("Full-Time Permanent")
    pages.employee_list.click_search()

    rows = pages.employee_list.get_table_rows()
    no_records = pages.employee_list.get_no_records_text()
    expect(rows.first.or_(no_records)).to_be_visible(timeout=10000)


def test_reset_clears_filters(pages):
    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_name("e")
    pages.employee_list.get_autocomplete_options().first.click()
    pages.employee_list.click_search()
    filtered_count = pages.employee_list.get_table_rows().count()

    pages.employee_list.click_reset()
    pages.employee_list.get_table_rows().first.wait_for(timeout=10000)
    reset_count = pages.employee_list.get_table_rows().count()

    assert reset_count >= filtered_count


def test_no_match_search_shows_empty_state(pages):
    pages.employee_list.goto()
    pages.employee_list.fill_search_employee_id("999999")
    pages.employee_list.click_search()

    expect(pages.employee_list.get_no_records_text()).to_be_visible(timeout=10000)
