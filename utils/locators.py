"""Centralized selectors and timeouts. Page objects import from here rather than
hardcoding selector strings inline."""


class Inputs:
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
    TOAST = ".oxd-toast"
    FORM = ".oxd-form"
    INPUT_GROUP = ".oxd-form-row .oxd-input-group, .oxd-form-row .oxd-input-field-bottom-space"
    FIELD_ERROR_MESSAGE = ".oxd-input-field-error-message"
    SELECT_TEXT = ".oxd-select-text"
    SELECT_OPTION = ".oxd-select-dropdown .oxd-select-option"
    AUTOCOMPLETE_INPUT = ".oxd-autocomplete-wrapper input"
    AUTOCOMPLETE_OPTION = ".oxd-autocomplete-option"
    TABLE_ROW = ".oxd-table-card"
    TABLE_CELL = ".oxd-table-cell"
    ROW_CHECKBOX_ICON = ".oxd-checkbox-input-icon"
    ROW_ACTION_DELETE = "button:has(.bi-trash)"
    ROW_ACTION_EDIT = "button:has(.bi-pencil-fill)"
    CONFIRM_DIALOG = "[role='dialog']"
    CONFIRM_DIALOG_BODY = ".oxd-dialog-content, .orangehrm-text-center-align"
    NO_RECORDS_TEXT = "text=No Records Found"


class LoginLocators:
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_ALERT = ".oxd-alert-content-text"


class UserManagementLocators:
    SEARCH_BUTTON = "button[type='submit']"
    RESET_BUTTON = "button[type='reset']"
    ADD_BUTTON_TEXT = "Add"
    SAVE_BUTTON_TEXT = "Save"
    # Search form field order (0-indexed within CommonLocators.INPUT_GROUP)
    USERNAME_FIELD_INDEX = 0
    USER_ROLE_FIELD_INDEX = 1
    EMPLOYEE_NAME_FIELD_INDEX = 2
    STATUS_FIELD_INDEX = 3
    # Add-user form field order
    ADD_USER_ROLE_INDEX = 0
    ADD_STATUS_INDEX = 1
    DELETE_SELECTED_BUTTON_TEXT = "Delete Selected"
    CONFIRM_YES_DELETE_TEXT = "Yes, Delete"
    CONFIRM_NO_CANCEL_TEXT = "No, Cancel"


class EmployeeListLocators:
    SEARCH_BUTTON = "button[type='submit']"
    RESET_BUTTON = "button[type='reset']"
    ADD_BUTTON_TEXT = "Add"
    SAVE_BUTTON_TEXT = "Save"
    # Search form field order
    EMPLOYEE_NAME_FIELD_INDEX = 0
    EMPLOYEE_ID_FIELD_INDEX = 1
    EMPLOYMENT_STATUS_FIELD_INDEX = 2
    # Add-employee form: text inputs are [Search(autocomplete internal), First, Middle, Last]
    FIRST_NAME_INPUT_INDEX = 1
    MIDDLE_NAME_INPUT_INDEX = 2
    LAST_NAME_INPUT_INDEX = 3
    DELETE_SELECTED_BUTTON_TEXT = "Delete Selected"
    CONFIRM_YES_DELETE_TEXT = "Yes, Delete"
    # Personal Details / detail-view
    EMPLOYEE_ID_INPUT_INDEX = 4


class LeaveListLocators:
    APPLY_BUTTON_TEXT = "Apply"
    ASSIGN_BUTTON_TEXT = "Assign"
    SEARCH_BUTTON = "button[type='submit']"
    RESET_BUTTON = "button[type='reset']"
    OK_BUTTON_TEXT = "Ok"
    APPROVE_BUTTON_TEXT = "Approve"
    REJECT_BUTTON_TEXT = "Reject"
    COMMENT_TEXTAREA = "textarea"
    DATE_INPUT = "input.oxd-input[placeholder='yyyy-dd-mm']"
    # Apply Leave form order: Leave Type(select), From Date, To Date, Comments
    APPLY_LEAVE_TYPE_SELECT_INDEX = 0
    # Assign Leave form order: Employee Name(autocomplete), Leave Type(select), From Date, To Date, Comments
    ASSIGN_LEAVE_TYPE_SELECT_INDEX = 0
    # Leave List filter form order: From Date, To Date, Show Leave with Status(select),
    # Leave Type(select), Employee Name(autocomplete), Sub Unit(select)
    STATUS_SELECT_INDEX = 2
    STATUS_TEXT_CELL_INDEX = 6


class InboxLocators:
    MESSAGE_LIST_CONTAINER = ".wrapper-primary-table.scrollbar"
    MESSAGE_ROW = ".wrapper-primary-table.scrollbar table tbody tr"
    ROW_FROM_CELL_INDEX = 1
    ROW_SUBJECT_CELL_INDEX = 2
    ROW_RECEIVED_CELL_INDEX = 3
    INBOX_NAME_INPUT = "#inbox_field"
    GO_BUTTON = "button.primary-btn"


class MessageDetailLocators:
    RAW_TAB = "#pills-raw-tab"
    RAW_CONTENT_PANE = "#pills-raw"
