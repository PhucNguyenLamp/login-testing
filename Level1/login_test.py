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


class LoginDataDrivenTest(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.driver.implicitly_wait(10)

    def test_login_data_driven(self):

        driver = self.driver

        with open("login_data.csv", newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                print("\nRunning:", row["testcase_id"])

                driver.get(
                    "https://school.moodledemo.net/login/index.php?loginredirect=1"
                )

                time.sleep(1)  # wait for page JS to fully settle

                wait = WebDriverWait(driver, 10)

                # INPUT FIELDS - use element_to_be_clickable to ensure element is
                # present, visible, AND interactable before each action.
                # This avoids StaleElementReferenceException from Moodle's JS re-rendering.
                wait.until(EC.element_to_be_clickable((By.ID, "username"))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(row["username"])

                wait.until(EC.element_to_be_clickable((By.ID, "password"))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(row["password"])

                # CLICK LOGIN
                driver.find_element(By.ID, "loginbtn").click()

                time.sleep(2)

                # =========================
                # FAILED LOGIN TEST CASES
                # =========================
                if row["expected_type"] == "fail":

                    error_text = driver.find_element(
                        By.ID,
                        "loginerrormessage"
                    ).text

                    self.assertIn(
                        row["expected_result"],
                        error_text
                    )

                # =========================
                # SUCCESS LOGIN TEST CASES
                # =========================
                elif row["expected_type"] == "success":

                    # Wait until URL no longer contains 'login' (redirected away from login page)
                    WebDriverWait(driver, 10).until(
                        EC.url_contains(row["expected_result"])
                    )

                    self.assertIn(
                        row["expected_result"],
                        driver.current_url
                    )

                    # LOG OUT after a successful login so the next test starts fresh.
                    # Deleting cookies is more reliable than hitting logout.php
                    # (which requires a sesskey token on newer Moodle versions).
                    driver.delete_all_cookies()
                    time.sleep(1)

                print("PASSED:", row["testcase_id"])

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()