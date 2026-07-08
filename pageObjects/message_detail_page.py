from utils.locators import Inputs, MessageDetailLocators


class MessageDetailPage:
    def __init__(self, page):
        self.page = page

    def click_raw_tab(self):
        self.page.locator(MessageDetailLocators.RAW_TAB).click()

    def get_raw_source_text(self):
        self.page.wait_for_function(
            "() => { const el = document.querySelector('%s'); "
            "return !!el && el.textContent.trim() !== ''; }" % MessageDetailLocators.RAW_CONTENT_PANE,
            timeout=Inputs.LONG_TIMEOUT,
        )
        return self.page.locator(MessageDetailLocators.RAW_CONTENT_PANE).text_content()
