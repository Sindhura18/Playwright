from utils.locators import Inputs, MessageDetailLocators


class MessageDetailPage:
    """Mailinator message detail view (raw source/headers)."""

    def __init__(self, page):
        self.page = page

    def click_raw_tab(self):
        self.page.locator(MessageDetailLocators.RAW_TAB).click()

    def get_raw_source_text(self):
        self.page.wait_for_function(
            "(id) => { const el = document.getElementById(id); "
            "return !!el && el.textContent.trim() !== ''; }",
            arg=MessageDetailLocators.RAW_CONTENT_PANE_ID,
            timeout=Inputs.LONG_TIMEOUT,
        )
        return self.page.locator(MessageDetailLocators.RAW_CONTENT_PANE).text_content()
