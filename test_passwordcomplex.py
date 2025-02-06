import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestPasswordComplexity():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_password_complexity(self):
        self.driver.get("https://localhost/users/request_account.php")
        self.driver.set_window_size(870, 1020)
        
        username = "testuser"
        first_name = "Test"
        last_name = "User"
        email = "testuser@example.com"
        weak_passwords = ["1234", "password", "admin"]

        for password in weak_passwords:
            # Fill in the account request form
            self.driver.find_element(By.ID, "first_name").clear()
            self.driver.find_element(By.ID, "first_name").send_keys(first_name)

            self.driver.find_element(By.ID, "last_name").clear()
            self.driver.find_element(By.ID, "last_name").send_keys(last_name)

            self.driver.find_element(By.ID, "email").clear()
            self.driver.find_element(By.ID, "email").send_keys(email)

            self.driver.find_element(By.ID, "username").clear()
            self.driver.find_element(By.ID, "username").send_keys(username)
            
            self.driver.find_element(By.ID, "password").clear()
            self.driver.find_element(By.ID, "password").send_keys(password)
            
            self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
            time.sleep(1)  # Adjust as needed for your application response time

            # Assert that the password was rejected
            assert "Password does not meet complexity requirements" in self.driver.page_source or "Password" in self.driver.page_source

            print(f"Password complexity test passed for: {password}")

        self.driver.close()
