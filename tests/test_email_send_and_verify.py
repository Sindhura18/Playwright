import os

from playwright.sync_api import expect
import pytest

from pageObjects.inbox_page import InboxPage
from utils.email_sender import send_test_email
from utils.helpers import unique_suffix

MAILINATOR_INBOX = os.getenv("MAILINATOR_INBOX", "zqautoframework")


@pytest.fixture(scope="module")
def sent_email():
    subject = f"ZQAuto Framework Test {unique_suffix()}"
    body = "This is an automated test email sent by the Playwright + pytest framework."
    to_address = send_test_email(MAILINATOR_INBOX, subject, body)
    return {"subject": subject, "body": body, "to_address": to_address}


@pytest.fixture(scope="module")
def inbox(mailinator_page, sent_email):
    # SMTP accepting the message only means Gmail queued it for relay, not that it has
    # reached Mailinator yet, so this waits out that delivery lag once for the module.
    page = InboxPage(mailinator_page)
    page.goto(MAILINATOR_INBOX)
    page.wait_for_message(sent_email["subject"])
    return page


def test_sent_email_appears_in_inbox_list(inbox, sent_email):
    subjects = inbox.get_all_subjects()
    assert any(sent_email["subject"] in subject for subject in subjects)


def test_sent_email_subject_matches_exactly(inbox, sent_email):
    subjects = inbox.get_all_subjects()
    matching = [s for s in subjects if sent_email["subject"] in s]
    assert len(matching) == 1


def test_inbox_row_count_increments_after_send(inbox, sent_email):
    count_before = inbox.get_message_rows().count()

    second_subject = f"{sent_email['subject']}-second"
    send_test_email(MAILINATOR_INBOX, second_subject, sent_email["body"])
    inbox.wait_for_message(second_subject)

    expect(inbox.get_message_rows()).to_have_count(count_before + 1, timeout=10000)


def test_sender_address_shown_in_inbox_row(inbox):
    rows = inbox.get_message_rows()
    row_count = rows.count()
    from_texts = [inbox.get_row_from(i) for i in range(row_count)]
    smtp_user = os.environ["SMTP_USER"]
    assert any(smtp_user in text for text in from_texts)


def test_never_sent_to_inbox_has_no_matching_message(inbox):
    subjects = inbox.get_all_subjects()
    assert not any("this-subject-was-never-sent" in subject for subject in subjects)
