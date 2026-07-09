from utils.locators import Inputs, InboxLocators


class InboxPage:
    """Mailinator public inbox message list."""

    def __init__(self, page):
        self.page = page

    def goto(self, inbox_name):
        url = Inputs.MAILINATOR_INBOX_URL.format(inbox=inbox_name)
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_selector(InboxLocators.MESSAGE_LIST_CONTAINER, timeout=Inputs.LONG_TIMEOUT)

    def get_message_rows(self):
        return self.page.locator(InboxLocators.MESSAGE_ROW)

    def get_row_subject(self, row_index):
        row = self.get_message_rows().nth(row_index)
        return row.locator(InboxLocators.TABLE_DATA_CELL).nth(InboxLocators.ROW_SUBJECT_CELL_INDEX).text_content()

    def get_row_from(self, row_index):
        row = self.get_message_rows().nth(row_index)
        return row.locator(InboxLocators.TABLE_DATA_CELL).nth(InboxLocators.ROW_FROM_CELL_INDEX).text_content()

    def get_all_subjects(self):
        rows = self.get_message_rows()
        return [
            rows.nth(i).locator(InboxLocators.TABLE_DATA_CELL).nth(InboxLocators.ROW_SUBJECT_CELL_INDEX).text_content()
            for i in range(rows.count())
        ]

    def click_row(self, row_index):
        self.get_message_rows().nth(row_index).click()

    def click_message_by_subject(self, subject):
        self.get_message_rows().filter(has_text=subject).first.click()

    def reload_inbox(self, inbox_name):
        self.goto(inbox_name)

    def wait_for_message(self, subject, timeout=Inputs.EMAIL_DELIVERY_TIMEOUT):
        """Polls the live, auto-updating inbox list for a subject rather than assuming
        it's already there - SMTP accepting a message only means it was queued for
        relay, delivery into Mailinator can still take seconds to tens of seconds."""
        self.page.wait_for_function(
            "(subject) => Array.from("
            "document.querySelectorAll('.wrapper-primary-table.scrollbar table tbody tr')"
            ").some((row) => row.innerText.includes(subject))",
            arg=subject,
            timeout=timeout,
        )
