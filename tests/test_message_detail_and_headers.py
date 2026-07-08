import os

import pytest

from pageObjects.inbox_page import InboxPage
from pageObjects.message_detail_page import MessageDetailPage
from utils.email_sender import send_test_email
from utils.helpers import unique_suffix
from utils.regex_patterns import Patterns

MAILINATOR_INBOX = os.getenv("MAILINATOR_INBOX", "zqautoframework")


@pytest.fixture(scope="module")
def sent_email():
    subject = f"ZQAuto Headers Test {unique_suffix()}"
    body = "Body content used to verify the Mailinator message detail view."
    to_address = send_test_email(MAILINATOR_INBOX, subject, body)
    return {"subject": subject, "body": body, "to_address": to_address}


@pytest.fixture(scope="module")
def opened_message(mailinator_page, sent_email):
    inbox = InboxPage(mailinator_page)
    inbox.goto(MAILINATOR_INBOX)
    inbox.wait_for_message(sent_email["subject"])
    inbox.click_message_by_subject(sent_email["subject"])
    detail = MessageDetailPage(mailinator_page)
    detail.click_raw_tab()
    return detail


def test_opened_message_subject_matches(opened_message, sent_email):
    raw_text = opened_message.get_raw_source_text()
    match = Patterns.SUBJECT_HEADER.search(raw_text)
    assert match is not None
    assert sent_email["subject"] in match.group(1)


def test_opened_message_body_contains_expected_content(opened_message, sent_email):
    # Emails sent by this suite are plain text, so Mailinator doesn't render an HTML
    # tab for them (it's hidden when a message has no HTML part) - the raw source
    # always includes the body after the headers regardless of content type.
    raw_text = opened_message.get_raw_source_text()
    assert sent_email["body"] in raw_text


def test_raw_source_exposes_headers(opened_message):
    raw_text = opened_message.get_raw_source_text()
    assert Patterns.FROM_HEADER.search(raw_text) is not None
    assert Patterns.SUBJECT_HEADER.search(raw_text) is not None


def test_raw_source_date_header_is_well_formed(opened_message):
    raw_text = opened_message.get_raw_source_text()
    match = Patterns.DATE_HEADER.search(raw_text)
    assert match is not None
    assert len(match.group(1).strip()) > 10


def test_from_address_matches_smtp_user(opened_message):
    raw_text = opened_message.get_raw_source_text()
    match = Patterns.FROM_HEADER.search(raw_text)
    assert match is not None
    assert os.environ["SMTP_USER"] in match.group(1)
