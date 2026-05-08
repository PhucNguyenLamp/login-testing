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


class LogoutLevel2Test(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.driver.implicitly_wait(10)

    def test_logout_level2(self):

        driver = self.driver

        with open("logout_data.csv", newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                # Skip blank lines in the CSV
                if not row.get("testcase_id", "").strip():
                    continue

                print("\nRunning:", row["testcase_id"])

                # -------------------------
                # STEP 1: Login — URL and field IDs come from CSV
                # -------------------------
                driver.get(row["url"])

                time.sleep(1)

                wait = WebDriverWait(driver, 10)

                wait.until(EC.element_to_be_clickable((By.ID, row["username_field"]))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, row["username_field"]))).send_keys(row["username"])

                wait.until(EC.element_to_be_clickable((By.ID, row["password_field"]))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, row["password_field"]))).send_keys(row["password"])

                wait.until(EC.element_to_be_clickable((By.ID, row["login_button"]))).click()

                wait.until(EC.url_contains("/my/"))

                # -------------------------
                # STEP 2: Logout — element IDs come from CSV
                # -------------------------
                driver.get("https://school.moodledemo.net/my/courses.php")

                wait.until(EC.element_to_be_clickable((By.ID, row["user_menu_id"]))).click()

                wait.until(EC.element_to_be_clickable((By.LINK_TEXT, row["logout_link_text"]))).click()

                time.sleep(2)

                # -------------------------
                # STEP 3: Assert expected result — value comes from CSV
                # -------------------------
                driver.get("https://school.moodledemo.net/")

                self.assertIn(
                    row["expected_result"],
                    driver.title
                )

                print("PASSED:", row["testcase_id"])

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
