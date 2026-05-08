# -*- coding: utf-8 -*-

import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class LoginPerformanceTest(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

    def test_login_response_time(self):

        driver = self.driver

        start_time = time.time()

        driver.get(
            "https://school.moodledemo.net/login/index.php?loginredirect=1"
        )

        driver.find_element(By.ID, "username").send_keys("teacher")
        driver.find_element(By.ID, "password").send_keys("moodle26")
        driver.find_element(By.ID, "loginbtn").click()

        end_time = time.time()

        response_time = end_time - start_time

        print("Login response time:", response_time, "seconds")

        # Requirement:
        # Login process must complete within 5 seconds
        self.assertLess(response_time, 5)

    def tearDown(self):

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()