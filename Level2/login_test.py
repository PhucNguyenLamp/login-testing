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


class LoginLevel2Test(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.driver.implicitly_wait(10)

    def test_login_level2(self):

        driver = self.driver

        with open("login_data.csv", newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                # Skip blank lines in the CSV
                if not row.get("testcase_id", "").strip():
                    continue

                print("\nRunning:", row["testcase_id"])

                # URL COMES FROM CSV
                driver.get(row["url"])

                # Wait for page JS to fully settle before locating elements
                time.sleep(1)

                wait = WebDriverWait(driver, 10)

                # ELEMENT IDS COME FROM CSV

                username_field = row["username_field"]
                password_field = row["password_field"]
                login_button = row["login_button"]
                error_selector = row["error_selector"]

                # USERNAME
                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, username_field)
                    )
                ).clear()

                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, username_field)
                    )
                ).send_keys(row["username"])

                # PASSWORD
                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, password_field)
                    )
                ).clear()

                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, password_field)
                    )
                ).send_keys(row["password"])

                # LOGIN BUTTON
                wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, login_button)
                    )
                ).click()

                time.sleep(2)

                # FAIL CASES
                if row["expected_type"] == "fail":

                    error_text = driver.find_element(
                        By.ID,
                        error_selector
                    ).text

                    self.assertIn(
                        row["expected_result"],
                        error_text
                    )

                # SUCCESS CASES
                elif row["expected_type"] == "success":

                    WebDriverWait(driver, 10).until(
                        EC.url_contains(
                            row["expected_result"]
                        )
                    )

                    self.assertIn(
                        row["expected_result"],
                        driver.current_url
                    )

                    driver.delete_all_cookies()

                print("PASSED:", row["testcase_id"])

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()