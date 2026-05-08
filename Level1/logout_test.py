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


class LogoutTest(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

        self.driver.implicitly_wait(10)

    def test_logout(self):

        driver = self.driver
        wait = WebDriverWait(driver, 10)

        with open("logout_data.csv", newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                # Skip blank lines
                if not row.get("testcase_id", "").strip():
                    continue

                print("\nRunning:", row["testcase_id"])

                # -------------------------
                # STEP 1: Login — credentials from CSV
                # -------------------------
                driver.get("https://school.moodledemo.net/login/index.php")

                time.sleep(1)

                wait.until(EC.element_to_be_clickable((By.ID, "username"))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(row["username"])

                wait.until(EC.element_to_be_clickable((By.ID, "password"))).clear()
                wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(row["password"])

                driver.find_element(By.ID, "loginbtn").click()

                wait.until(EC.url_contains("/my/"))

                # -------------------------
                # STEP 2: Log out via user menu
                # -------------------------
                driver.get("https://school.moodledemo.net/my/courses.php")

                wait.until(EC.element_to_be_clickable((By.ID, "user-menu-toggle"))).click()

                wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log out"))).click()

                time.sleep(2)

                # -------------------------
                # STEP 3: Assert expected result — value from CSV
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
