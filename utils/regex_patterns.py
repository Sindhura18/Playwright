import re


class Patterns:
    """Compiled regexes used to parse text pulled off pages by test files.
    No Playwright objects/assertions live here - pure string parsing only."""

    SUBJECT_HEADER = re.compile(r"^Subject:\s*(.+)$", re.MULTILINE)
    FROM_HEADER = re.compile(r"^From:\s*(.+)$", re.MULTILINE)
    TO_HEADER = re.compile(r"^To:\s*(.+)$", re.MULTILINE)
    DATE_HEADER = re.compile(r"^Date:\s*(.+)$", re.MULTILINE)
    MESSAGE_ID_HEADER = re.compile(r"^Message-ID:\s*(.+)$", re.MULTILINE | re.IGNORECASE)

    EMAIL_ADDRESS = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
    EMPLOYEE_ID = re.compile(r"^\d+$")
    LEAVE_STATUS_WITH_DAYS = re.compile(r"^(.+?)\s*\(([\d.]+)\)$")
