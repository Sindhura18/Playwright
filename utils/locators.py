"""Centralized XPath selectors and timeouts, imported by page objects rather than
hardcoded inline."""


def has_class(name):
    """XPath predicate matching a class as a whole word (plain contains(@class,'x')
    also matches unrelated OXD classes that share a prefix, e.g. 'oxd-table-card'
    would match 'oxd-table-card-cell-checkbox' too)."""
    return f"contains(concat(' ', normalize-space(@class), ' '), ' {name} ')"


class Inputs:
    """Timeouts and OrangeHRM/Mailinator URL paths."""
    DEFAULT_TIMEOUT = 10000
    SHORT_TIMEOUT = 5000
    LONG_TIMEOUT = 30000
    EMAIL_DELIVERY_TIMEOUT = 60000

    ORANGEHRM_LOGIN_PATH = "/web/index.php/auth/login"
    ORANGEHRM_DASHBOARD_PATH = "/web/index.php/dashboard/index"
    ADMIN_USERS_PATH = "/web/index.php/admin/viewSystemUsers"
    ADMIN_ADD_USER_PATH = "/web/index.php/admin/saveSystemUser"
    PIM_EMPLOYEE_LIST_PATH = "/web/index.php/pim/viewEmployeeList"
    PIM_ADD_EMPLOYEE_PATH = "/web/index.php/pim/addEmployee"
    LEAVE_APPLY_PATH = "/web/index.php/leave/applyLeave"
    LEAVE_ASSIGN_PATH = "/web/index.php/leave/assignLeave"
    LEAVE_LIST_PATH = "/web/index.php/leave/viewLeaveList"

    MAILINATOR_INBOX_URL = "https://www.mailinator.com/v4/public/inboxes.jsp?to={inbox}"


class CommonLocators:
    """Shared OrangeHRM OXD component selectors reused across several pages."""
    TOAST = f"//*[{has_class('oxd-toast')}]"
    FORM = f"//*[{has_class('oxd-form')}]"
    INPUT_GROUP = (
        f"//*[{has_class('oxd-form-row')}]//*[{has_class('oxd-input-group')}]"
        f" | //*[{has_class('oxd-form-row')}]//*[{has_class('oxd-input-field-bottom-space')}]"
    )
    FIELD_ERROR_MESSAGE = f"//*[{has_class('oxd-input-field-error-message')}]"
    SELECT_TEXT = f"//*[{has_class('oxd-select-text')}]"
    SELECT_OPTION = f"//*[{has_class('oxd-select-dropdown')}]//*[{has_class('oxd-select-option')}]"
    AUTOCOMPLETE_INPUT = f"//*[{has_class('oxd-autocomplete-wrapper')}]//input"
    AUTOCOMPLETE_OPTION = f"//*[{has_class('oxd-autocomplete-option')}]"
    TABLE_ROW = f"//*[{has_class('oxd-table-card')}]"
    TABLE_CELL = f"//*[{has_class('oxd-table-cell')}]"
    ROW_CHECKBOX_ICON = f"//*[{has_class('oxd-checkbox-input-icon')}]"
    ROW_ACTION_DELETE = f"//button[.//*[{has_class('bi-trash')}]]"
    ROW_ACTION_EDIT = f"//button[.//*[{has_class('bi-pencil-fill')}]]"
    CONFIRM_DIALOG = "//*[@role='dialog']"
    CONFIRM_DIALOG_BODY = f"//*[{has_class('oxd-dialog-content')}] | //*[{has_class('orangehrm-text-center-align')}]"
    # Exact text() equality: Playwright's XPath evaluator doesn't reliably match
    # contains(text(), 'x'), since text() returns a node-set.
    NO_RECORDS_TEXT = "//*[text()='No Records Found']"
    GENERIC_INPUT = "//input"
    GENERIC_OXD_INPUT = f"//input[{has_class('oxd-input')}]"


class LoginLocators:
    """Login page."""
    USERNAME_INPUT = "//input[@name='username']"
    PASSWORD_INPUT = "//input[@name='password']"
    LOGIN_BUTTON = "//button[@type='submit']"
    ERROR_ALERT = f"//*[{has_class('oxd-alert-content-text')}]"
    DASHBOARD_LOADED_INDICATOR = f"//h6[{has_class('oxd-text--h6')}]"


class UserManagementLocators:
    """Admin > User Management (System Users) search, add, and row-action forms."""
    SEARCH_BUTTON_TEXT = "Search"
    RESET_BUTTON_TEXT = "Reset"
    ADD_BUTTON_TEXT = "Add"
    SAVE_BUTTON_TEXT = "Save"
    # Field order within CommonLocators.INPUT_GROUP on the search form
    USERNAME_FIELD_INDEX = 0
    USER_ROLE_FIELD_INDEX = 1
    EMPLOYEE_NAME_FIELD_INDEX = 2
    STATUS_FIELD_INDEX = 3
    # Field order on the add-user form
    ADD_USER_ROLE_INDEX = 0
    ADD_STATUS_INDEX = 1
    # Add-user text inputs, in DOM order: [autocomplete-internal, username, password, confirm]
    ADD_USERNAME_INPUT_INDEX = 1
    ADD_PASSWORD_INPUT_INDEX = 2
    ADD_CONFIRM_PASSWORD_INPUT_INDEX = 3
    DELETE_SELECTED_BUTTON_TEXT = "Delete Selected"
    CONFIRM_YES_DELETE_TEXT = "Yes, Delete"
    CONFIRM_NO_CANCEL_TEXT = "No, Cancel"


class EmployeeListLocators:
    """PIM > Employee List: search, add-employee form, and Personal Details view."""
    SEARCH_BUTTON_TEXT = "Search"
    RESET_BUTTON_TEXT = "Reset"
    ADD_BUTTON_TEXT = "Add"
    SAVE_BUTTON_TEXT = "Save"
    EMPLOYEE_NAME_FIELD_INDEX = 0
    EMPLOYEE_ID_FIELD_INDEX = 1
    EMPLOYMENT_STATUS_FIELD_INDEX = 2
    # Add-employee text inputs, in DOM order: [autocomplete-internal, First, Middle, Last]
    FIRST_NAME_INPUT_INDEX = 1
    MIDDLE_NAME_INPUT_INDEX = 2
    LAST_NAME_INPUT_INDEX = 3
    FIRST_NAME_INPUT = "//input[@name='firstName']"
    LAST_NAME_INPUT = "//input[@name='lastName']"
    DELETE_SELECTED_BUTTON_TEXT = "Delete Selected"
    CONFIRM_YES_DELETE_TEXT = "Yes, Delete"
    EMPLOYEE_ID_INPUT_INDEX = 4
    PAGE_HEADING = f"//h6[{has_class('orangehrm-main-title')}]"


class LeaveListLocators:
    """Leave > Apply, Assign Leave, and Leave List (approve/reject/filter)."""
    APPLY_BUTTON_TEXT = "Apply"
    ASSIGN_BUTTON_TEXT = "Assign"
    SEARCH_BUTTON_TEXT = "Search"
    RESET_BUTTON_TEXT = "Reset"
    OK_BUTTON_TEXT = "Ok"
    APPROVE_BUTTON_TEXT = "Approve"
    REJECT_BUTTON_TEXT = "Reject"
    COMMENT_TEXTAREA = "//textarea"
    DATE_INPUT = f"//input[{has_class('oxd-input')} and @placeholder='yyyy-dd-mm']"
    # Apply Leave order: Leave Type(select), From Date, To Date, Comments
    APPLY_LEAVE_TYPE_SELECT_INDEX = 0
    # Assign Leave order: Employee Name(autocomplete), Leave Type(select), From Date, To Date, Comments
    ASSIGN_LEAVE_TYPE_SELECT_INDEX = 0
    # Leave List filter order: From/To Date, Status(select), Leave Type(select),
    # Employee Name(autocomplete), Sub Unit(select)
    STATUS_SELECT_INDEX = 2
    STATUS_TEXT_CELL_INDEX = 6


class InboxLocators:
    """Mailinator public inbox message list."""
    MESSAGE_LIST_CONTAINER = f"//*[{has_class('wrapper-primary-table')} and {has_class('scrollbar')}]"
    MESSAGE_ROW = f"//*[{has_class('wrapper-primary-table')} and {has_class('scrollbar')}]//table//tr"
    ROW_FROM_CELL_INDEX = 1
    ROW_SUBJECT_CELL_INDEX = 2
    ROW_RECEIVED_CELL_INDEX = 3
    TABLE_DATA_CELL = "//td"
    INBOX_NAME_INPUT = "//*[@id='inbox_field']"
    GO_BUTTON = f"//button[{has_class('primary-btn')}]"


class MessageDetailLocators:
    """Mailinator message detail view (raw source tab)."""
    RAW_TAB = "//*[@id='pills-raw-tab']"
    RAW_CONTENT_PANE = "//*[@id='pills-raw']"
    RAW_CONTENT_PANE_ID = "pills-raw"
