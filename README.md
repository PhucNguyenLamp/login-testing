# Selenium Data-Driven Testing — Mount Orange (Moodle Demo)

Automated test suite using **Python `unittest` + Selenium WebDriver** against the [Mount Orange Moodle Demo](https://school.moodledemo.net). Tests are structured across two levels of data-driven maturity and a non-functional test.

---

## Project Structure

```
.
├── Level1/                      # Data-driven: test data in CSV
│   ├── login_test.py
│   ├── login_data.csv
│   ├── logout_test.py
│   ├── logout_data.csv
│   ├── guest_login_test.py
│   └── guest_login_data.csv
│
├── Level2/                      # Data-driven: test data AND element selectors in CSV
│   ├── login_test.py
│   ├── login_data.csv
│   ├── logout_test.py
│   ├── logout_data.csv
│   ├── guest_login_test.py
│   └── guest_login_data.csv
│
├── NonFunctional/
│   └── nonfunctional_performance_test.py
│
└── ImplementDataDrivenTesting/  # Original Katalon-exported test cases (reference)
    ├── TC001001.py — TC001012.py
```

---

## Test Cases

### Functional — Login (`TC-001-001` to `TC-001-009`)

Tests the login form on `school.moodledemo.net` with a range of valid and invalid inputs.

| Test Case | Username | Password | Expected |
|---|---|---|---|
| TC-001-001 | *(empty)* | moodle26 | Fail — error message shown |
| TC-001-002 | `a` | moodle26 | Fail — error message shown |
| TC-001-003 | teacher | *(empty)* | Fail — error message shown |
| TC-001-004 | teacher | `m` | Fail — error message shown |
| TC-001-005 | *(64-char string)* | `m` | Fail — error message shown |
| TC-001-006 | teacher | moodle26 | **Success** — redirected to `/my/` |
| TC-001-007 | teacher | wrongpass | Fail — error message shown |
| TC-001-008 | fakeuser999 | moodle26 | Fail — error message shown |
| TC-001-009 | *(empty)* | *(empty)* | Fail — error message shown |

### Functional — Logout (`TC-011-001`)

Logs in as `teacher`, navigates to the user menu, clicks **Log out**, and asserts the page title returns to `"Mount Orange"`.

### Functional — Guest Login (`TC-012-001`)

Clears browser cookies (to ensure the guest button is visible), clicks **Log in as a guest**, and asserts the page contains `"You are currently using guest access"`.

### Non-Functional — Performance (`NonFunctional/`)

Measures the time from page load → credentials entered → login button clicked. Asserts the total time is **under 5 seconds**.

> Result: ~3.9 seconds ✅

---

## Level 1 vs Level 2

| | Level 1 | Level 2 |
|---|---|---|
| **Test data in CSV** | ✅ (credentials, expected results) | ✅ |
| **Element selectors in CSV** | ❌ (hardcoded in test) | ✅ (IDs read from CSV) |
| **URL in CSV** | ❌ (hardcoded in test) | ✅ |
| **Reusability** | Same site only | Any site with matching structure |

**Level 1** is suitable when the site under test is fixed — selectors are hardcoded but test data (credentials, expected text) comes from the CSV.

**Level 2** is fully parameterised — the URL, all element IDs, and expected results are in the CSV, so the same test script can be pointed at a different site just by changing the CSV.

---

## How to Run

> Make sure you are `cd`'d into the correct folder before running.

```bash
# Level 1
cd Level1
python login_test.py
python logout_test.py
python guest_login_test.py

# Level 2
cd Level2
python login_test.py
python logout_test.py
python guest_login_test.py

# Non-Functional
cd NonFunctional
python nonfunctional_performance_test.py
```

---

## Requirements

```
selenium
webdriver-manager
```

Install with:

```bash
pip install selenium webdriver-manager
```

ChromeDriver is managed automatically via `webdriver-manager` — no manual setup needed.

---

## Notes

- The Mount Orange demo site **resets every hour** and credentials change (e.g. `moodle25` → `moodle26`). Update the password in the CSV files if tests fail after a reset.
- A `time.sleep(1)` after each `driver.get()` is intentional — Moodle's JS re-renders the login form after page load, which causes `StaleElementReferenceException` without it.
- After a successful login test case, `driver.delete_all_cookies()` clears the session so the next row starts fresh on the login page.
- The guest login button disappears if a session cookie already exists — cookies are cleared before each guest login test for this reason.
