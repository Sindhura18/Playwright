# Playwright (Python) + pytest Test Automation Framework

A Page-Object-Model test suite built with Playwright's **sync API** and **pytest**,
demonstrating search, filtering, bulk actions, approve/reject workflows, CRUD, and
detail-view validation against two public targets — plus a send-and-verify email flow
built on real SMTP + a public inbox.

## What this tests, and why these two targets

| Target | What's exercised |
|---|---|
| [OrangeHRM open-source demo](https://opensource-demo.orangehrmlive.com/) | Login, Admin > User Management (search/filter/bulk delete), PIM > Employee List (search/filter/CRUD/detail view), Leave (assign/approve/reject) |
| [Mailinator](https://www.mailinator.com/) public inbox | Send a real email via SMTP, verify it lands in a public inbox, open it and inspect the message detail/raw headers |

**OrangeHRM is a common, well-known practice target** — plenty of tutorials automate
its login form. That's deliberate, not accidental: the point of this repo isn't to
prove the app is testable (it obviously is), it's to show a specific set of engineering
decisions applied consistently across a real, moderately complex app:

- A strict Page Object boundary (see [Architecture](#architecture) below) enforced by
  hand across every page object in this repo — locators and interactions only, zero
  assertions.
- Test data that's created and cleaned up per-scenario (throwaway users/employees with
  randomized suffixes) rather than relying on fixed seed data, because this demo is
  public and shared with everyone else automating against it at the same time.
- Honest handling of a shared, uncontrolled environment: a few scenarios in
  `test_leave_approve_reject.py` `skip` (not fail) when the shared demo currently has no
  pending leave requests from other users — see [Known limitations](#known-limitations-of-a-shared-public-demo).
- A CI story: this suite is designed to be dropped into the Jenkins pipeline already in
  this repo ([`Jenkinsfile`](Jenkinsfile)) and re-run on a schedule (a cron-triggered
  Jenkins job every N hours) — that recurring-run setup is the actual point of the
  "continuous verification" idea, not a demo-only concept faked in the UI.

The differentiator is the **framework design and the CI loop around it**, not the
application under test.

## Architecture

```
Playwright/
├── conftest.py            # logger, browser, orangehrm_login, pages, mailinator_page fixtures
├── pageObjects/            # locators + interactions ONLY - no assert/expect here
│   ├── login_page.py
│   ├── user_management_page.py
│   ├── employee_list_page.py
│   ├── leave_list_page.py
│   ├── inbox_page.py
│   └── message_detail_page.py
├── utils/                   # pure functions - no Playwright assertions
│   ├── helpers.py           # retry_action, unique_suffix, set_date_field, debug_pause
│   ├── locators.py          # Inputs (timeouts) + one selector class per page
│   ├── email_sender.py       # send_test_email() via smtplib
│   └── regex_patterns.py    # Patterns - header/email regexes for test-file parsing
└── tests/                    # all assertions, waits-with-expect, and workflows live here
```

**Hard rule, enforced throughout:** page objects expose only `goto`, `click_*`,
`fill_*`, `select_*`, `get_locator`, and `get_*_text`/`get_*_value` methods. Every
`expect(...)` assertion and every multi-step workflow ("assign leave → filter →
approve → verify status") lives in the test files, never in a page object. `utils/`
holds only pure Python — string/regex parsing, retry loops — never a Playwright
assertion.

Login happens once per **test file** (a module-scoped `orangehrm_login` fixture in
`conftest.py` logs in once and hands the authenticated page to every test in that
file via the `pages` fixture), not once per test and not once for the whole suite —
that keeps each file independently runnable without one file's data changes silently
affecting another's ordering.

`page.pause()` is available as `utils.helpers.debug_pause(page)`, but it's a no-op
unless `DEBUG_PAUSE=true` is set in the environment. Left ungated, a real
`page.pause()` blocks forever waiting for a human to click Resume in the Inspector —
that would hang an unattended Jenkins cron run. All real synchronization in this suite
uses `wait_for_selector` / `wait_for_function` / Playwright's auto-waiting `expect(...)`,
never a fixed sleep.

## Architecture note: the email piece

```
utils/email_sender.py  --SMTP-->  Gmail  --relay-->  Mailinator public inbox
                                                            │
                                                  pageObjects/inbox_page.py
                                                  (Playwright verifies the
                                                   message appears in the list)
                                                            │
                                                  pageObjects/message_detail_page.py
                                                  (Playwright opens it and reads
                                                   the raw source / headers)
```

`send_test_email()` sends a real email over SMTP (Gmail, using an App Password — not
your login password, Gmail always rejects that for SMTP) to `<inbox>@mailinator.com`.
Mailinator's public inboxes need no account or signup: anyone can send to any address
at that domain, and anyone who knows the inbox name can view it at
`https://www.mailinator.com/v4/public/inboxes.jsp?to=<inbox>`.

SMTP accepting the message only means Gmail queued it for relay, not that it has
already reached Mailinator — delivery can take anywhere from a couple of seconds to
under a minute. `InboxPage.wait_for_message(subject)` polls the live (auto-updating)
inbox list for that specific subject rather than assuming an immediate arrival, which
is what makes the two email test files reliable rather than racy.

## How to run locally

```bash
python -m venv .venv
source .venv/bin/activate        # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m playwright install chromium

cp .env.example .env             # then fill in the values below
pytest
```

`.env` values:

| Variable | Purpose |
|---|---|
| `ORANGEHRM_URL` / `ORANGEHRM_USER` / `ORANGEHRM_PASS` | defaults already point at the public demo (`Admin` / `admin123`) |
| `SMTP_USER` | a Gmail address to send test emails from |
| `SMTP_APP_PASSWORD` | a 16-character **App Password** for that account ([myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords), requires 2-Step Verification turned on first) — your regular password will not work |
| `MAIL_DOMAIN` | defaults to `mailinator.com` |
| `MAILINATOR_INBOX` | any inbox name you want to use as the destination |
| `HEADLESS` | `true` (default) or `false` to watch the browser locally |
| `DEBUG_PAUSE` | `true` to enable real `page.pause()` breakpoints; leave unset/`false` otherwise |

Running a single file or scenario works as usual:

```bash
pytest tests/test_employee_crud.py -v
pytest tests/test_login.py::test_valid_login_reaches_dashboard -v
```

A self-contained HTML report is written to `report.html` after every run
(`pytest.ini` sets `--html=report.html --self-contained-html`), and failure
screenshots land in `screenshots/` (both gitignored).

## Known limitations of a shared public demo

OrangeHRM's demo is public and reset/repopulated by everyone automating against it at
the same time — some of what looked like bugs during development turned out to be real
application behavior worth documenting:

- **Leave assigned via "Assign Leave"** (an admin granting leave on someone's behalf)
  is saved directly into `Scheduled` status — it never needs approval, so it never
  shows up in the Pending Approval view. Only self-service **Apply Leave** requests do,
  and the same account that applied can't approve/reject its own request. So
  `test_leave_approve_reject.py`'s approve/reject/filter scenarios act on whatever
  ambient Pending Approval requests other users' automation has left in the shared
  list, and `pytest.skip` (not fail) on the rare occasion none currently exist — that
  reflects real shared-environment state, not a defect in this suite.
- Several search/autocomplete fields only match employees who don't already have a
  linked resource (e.g. Admin's "Add User" employee picker only offers employees
  without an existing account) — tests use broad, resilient queries (e.g. a single
  common letter) rather than one fixed name, since a fixed name can be fully consumed
  by repeated runs (this suite's own, or anyone else's).
- The shared demo can occasionally respond slowly under concurrent load from everyone
  else automating against it; timeouts throughout this suite are set generously to
  absorb that rather than to mask a real defect.

## Screenshots of a passing run

Self-contained pytest-html report (0 failed, 41 passed, 4 skipped):

![pytest-html report summary](docs/screenshots/pytest_html_report.png)

OrangeHRM PIM > Employee List, mid-suite:

![OrangeHRM employee list](docs/screenshots/orangehrm_employee_list.png)

Mailinator public inbox showing delivered test emails:

![Mailinator inbox](docs/screenshots/mailinator_inbox.png)
