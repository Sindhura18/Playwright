import os
import uuid


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


def debug_pause(page):
    """Opens the Playwright Inspector and blocks until manually resumed - only when
    DEBUG_PAUSE=true is set in the environment. Left unset (the default), this is a
    no-op so headless/CI/Jenkins-cron runs never hang waiting on a human."""
    if os.getenv("DEBUG_PAUSE", "false").lower() == "true":
        page.pause()
