import os
import time
import uuid


def retry_action(fn, retries=3, delay=1.0):
    """Call fn() up to `retries` times, sleeping `delay` seconds between attempts,
    re-raising the last exception if every attempt fails."""
    last_exc = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - intentionally broad, this is a generic retry
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(delay)
    raise last_exc


def unique_suffix():
    """Short, time-based unique string for building throwaway usernames/employee names
    so tests don't collide with each other or with other users of the shared demo."""
    return uuid.uuid4().hex[:8]


def set_date_field(page, locator, value):
    """Clear an OrangeHRM date input (which doesn't clear on a plain .fill()) and type
    a fresh yyyy-dd-mm value."""
    locator.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    locator.type(value, delay=20)


def get_css_property(locator, property_name):
    return locator.evaluate(
        "(el, prop) => getComputedStyle(el).getPropertyValue(prop)", property_name
    )


def parse_table_row_texts(row_locator):
    """Return the trimmed text content of every cell in a table row locator."""
    cells = row_locator.locator(".oxd-table-cell")
    return [cells.nth(i).text_content().strip() for i in range(cells.count())]


def debug_pause(page):
    """Opens the Playwright Inspector and blocks until manually resumed - only when
    DEBUG_PAUSE=true is set in the environment. Left unset (the default), this is a
    no-op so headless/CI/Jenkins-cron runs never hang waiting on a human."""
    if os.getenv("DEBUG_PAUSE", "false").lower() == "true":
        page.pause()
