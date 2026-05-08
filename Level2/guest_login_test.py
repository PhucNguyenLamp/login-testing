# -*- coding: utf-8 -*-

import csv
import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class GuestLoginLevel2Test(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.driver.implicitly_wait(10)

    def test_guest_login_level2(self):

        driver = self.driver

        with open("guest_login_data.csv", newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                # Skip blank lines in the CSV
                if not row.get("testcase_id", "").strip():
                    continue

                print("\nRunning:", row["testcase_id"])

                # -------------------------
                # STEP 1: Clear cookies so guest button is always visible
                # URL comes from CSV
                # -------------------------
                driver.get(row["url"])
                driver.delete_all_cookies()

                # Navigate again with clean session
                driver.get(row["url"])

                time.sleep(1)

                wait = WebDriverWait(driver, 10)

                # -------------------------
                # STEP 2: Click guest login button — element ID comes from CSV
                # -------------------------
                wait.until(
                    EC.element_to_be_clickable((By.ID, row["guest_button_id"]))
                ).click()

                time.sleep(2)

                # -------------------------
                # STEP 3: Assert guest access — expected text comes from CSV
                # -------------------------
                self.assertIn(
                    row["expected_text"],
                    driver.page_source
                )

                print("PASSED:", row["testcase_id"])

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
