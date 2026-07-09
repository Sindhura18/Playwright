import datetime

import pytest
from playwright.sync_api import expect

from utils.locators import CommonLocators

# This is a shared public demo instance that many other automated test suites hit
# concurrently (visible in seeded comments like "Automated leave request via Selenium").
# Leave requests created here via Assign Leave were confirmed (via direct inspection)
# to be admin-assigned directly into "Scheduled" status - they never need approval, so
# they never appear in the Leave List/Pending Approval view. Only self-service Apply
# Leave requests land in Pending Approval, and those can't be approved/rejected by the
# same admin who applied (self-approval is blocked), and freshly created throwaway
# employees/ESS users have no configured leave entitlement to apply against either. So
# the approve/reject/filter scenarios act on whatever ambient Pending Approval requests
# other tenants' automation has left in the shared list, and skip (rather than fail)
# on the rare occasion none currently exist - that reflects real shared-environment
# state, not a defect in this suite.


def _future_weekday(days_ahead):
    date = datetime.date.today() + datetime.timedelta(days=days_ahead)
    while date.weekday() >= 5:
        date += datetime.timedelta(days=1)
    return date.strftime("%Y-%d-%m")


def _assign_leave_to(pages, employee_first_name, date_value):
    pages.leave_list.goto_assign()
    pages.leave_list.fill_employee_name(employee_first_name)
    pages.leave_list.get_autocomplete_options().first.click()
    pages.leave_list.select_leave_type(1)
    pages.leave_list.fill_from_date(date_value)
    pages.leave_list.fill_to_date(date_value)
    pages.leave_list.click_assign()
    try:
        pages.leave_list.get_ok_button().wait_for(timeout=3000)
        pages.leave_list.click_ok_confirm()
    except Exception:
        pass
    expect(pages.leave_list.get_toast()).to_contain_text("Success", timeout=10000)


def _pending_approval_rows(pages):
    pages.leave_list.goto_list()
    pages.leave_list.select_status_filter("Pending Approval")
    pages.leave_list.click_search()
    pages.leave_list.page.wait_for_timeout(1500)
    rows = pages.leave_list.get_table_rows()
    if rows.count() == 0:
        pytest.skip("No Pending Approval leave requests currently exist on the shared demo")
    return rows


def test_assign_leave_creates_a_scheduled_request(pages):
    # A wide, time-based offset avoids colliding with a date this suite (or another
    # concurrent run) already assigned leave against, which triggers a separate
    # "Overlapping Leave Request(s) Found" dialog this flow doesn't handle.
    days_ahead = 60 + (int(datetime.datetime.now().timestamp()) % 240)
    _assign_leave_to(pages, "e", _future_weekday(days_ahead))


def test_filter_leave_list_by_pending_approval(pages):
    rows = _pending_approval_rows(pages)
    row_count = rows.count()
    for i in range(row_count):
        assert "Pending Approval" in pages.leave_list.get_row_status_text(i)


def test_approve_first_pending_request(pages):
    _pending_approval_rows(pages)

    pages.leave_list.click_row_approve(0)
    expect(pages.leave_list.get_toast()).to_contain_text("Success", timeout=10000)


def test_reject_next_pending_request(pages):
    _pending_approval_rows(pages)

    pages.leave_list.click_row_reject(0)
    expect(pages.leave_list.get_toast()).to_contain_text("Success", timeout=10000)


def test_filter_by_employee_name_narrows_results(pages):
    rows = _pending_approval_rows(pages)
    total_count = rows.count()
    employee_name = rows.first.locator(CommonLocators.TABLE_CELL).nth(2).text_content().strip().split()[0]

    pages.leave_list.goto_list()
    pages.leave_list.fill_filter_employee_name(employee_name)
    pages.leave_list.click_search()
    filtered_rows = pages.leave_list.get_table_rows()
    expect(filtered_rows.first).to_be_visible(timeout=10000)

    assert filtered_rows.count() <= total_count
    for i in range(filtered_rows.count()):
        expect(filtered_rows.nth(i)).to_contain_text(employee_name)
