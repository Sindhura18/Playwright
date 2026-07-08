import re

from playwright.sync_api import expect

from utils.helpers import unique_suffix


def _add_employee(pages, first_name, last_name):
    pages.employee_list.goto_add_employee()
    pages.employee_list.fill_first_name(first_name)
    pages.employee_list.fill_last_name(last_name)
    pages.employee_list.click_save()
    pages.employee_list.wait_for_personal_details_page()


def test_personal_details_shows_created_employee_name(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "Detail"
    _add_employee(pages, first_name, last_name)

    full_name_value = pages.employee_list.get_employee_full_name_value()
    assert first_name in full_name_value
    assert last_name in full_name_value


def test_employee_id_field_is_present_and_non_empty(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "IdCheck"
    _add_employee(pages, first_name, last_name)

    employee_id_value = pages.employee_list.get_employee_id_value()
    assert employee_id_value.strip() != ""


def test_navigating_to_contact_details_tab_loads_section(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "ContactTab"
    _add_employee(pages, first_name, last_name)

    pages.employee_list.click_detail_tab("Contact Details")
    expect(pages.employee_list.page).to_have_url(re.compile("contactDetails"), timeout=10000)


def test_navigating_to_job_tab_loads_section(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "JobTab"
    _add_employee(pages, first_name, last_name)

    pages.employee_list.click_detail_tab("Job")
    expect(pages.employee_list.page).to_have_url(re.compile("viewJobDetails"), timeout=10000)


def test_edited_employee_id_reflects_on_detail_view(pages):
    first_name = f"ZQAuto{unique_suffix()}"
    last_name = "EditReflect"
    _add_employee(pages, first_name, last_name)

    new_employee_id = unique_suffix()
    pages.employee_list.fill_employee_id(new_employee_id)
    pages.employee_list.click_save_personal_details()
    expect(pages.employee_list.get_toast()).to_contain_text("Successfully Updated", timeout=10000)

    assert pages.employee_list.get_employee_id_value() == new_employee_id
