import re


class Patterns:
    """Compiled regexes used to parse text pulled off pages by test files.
    No Playwright objects/assertions live here - pure string parsing only."""

    SUBJECT_HEADER = re.compile(r"^Subject:\s*(.+)$", re.MULTILINE)
    FROM_HEADER = re.compile(r"^From:\s*(.+)$", re.MULTILINE)
    DATE_HEADER = re.compile(r"^Date:\s*(.+)$", re.MULTILINE)
