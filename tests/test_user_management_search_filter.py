from playwright.sync_api import expect


def test_search_by_username(pages):
    pages.user_management.goto()
    pages.user_management.fill_search_username("Admin")
    pages.user_management.click_search()

    rows = pages.user_management.get_table_rows()
    expect(rows).to_have_count(1, timeout=10000)
    expect(rows.first).to_contain_text("Admin")


def test_search_by_user_role(pages):
    pages.user_management.goto()
    pages.user_management.select_search_user_role("Admin")
    pages.user_management.click_search()

    rows = pages.user_management.get_table_rows()
    expect(rows.first).to_be_visible(timeout=10000)
    expect(rows.first).to_contain_text("Admin")


def test_search_by_nonexistent_username_shows_no_records(pages):
    pages.user_management.goto()
    pages.user_management.fill_search_username("no-such-user-zqauto")
    pages.user_management.click_search()

    expect(pages.user_management.get_no_records_text()).to_be_visible(timeout=10000)


def test_search_by_status(pages):
    pages.user_management.goto()
    pages.user_management.fill_search_username("Admin")
    pages.user_management.select_search_status("Enabled")
    pages.user_management.click_search()

    rows = pages.user_management.get_table_rows()
    expect(rows).to_have_count(1, timeout=10000)
    expect(rows.first).to_contain_text("Enabled")


def test_reset_restores_full_list(pages):
    pages.user_management.goto()
    pages.user_management.fill_search_username("Admin")
    pages.user_management.click_search()
    filtered_count = pages.user_management.get_table_rows().count()

    pages.user_management.click_reset()
    pages.user_management.page.wait_for_timeout(1500)
    pages.user_management.get_table_rows().first.wait_for(timeout=10000)
    reset_count = pages.user_management.get_table_rows().count()

    assert reset_count >= filtered_count
