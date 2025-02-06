import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestBruteForceLockout:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_brute_force_lockout(self):
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)
        
        username = "admin"
        incorrect_password = "wrongpassword"
        
        for _ in range(5):  # Adjust this number based on your lockout policy
            self.driver.find_element(By.ID, "username").clear()
            self.driver.find_element(By.ID, "username").send_keys(username)
            
            self.driver.find_element(By.ID, "password").clear()
            self.driver.find_element(By.ID, "password").send_keys(incorrect_password)
            
            self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
            time.sleep(1)  # Adjust as needed for your application response time

        # Attempt to log in again after the account should be locked
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(incorrect_password)
        
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        time.sleep(1)  # Adjust as needed for your application response time
        
        # Assert that the account is locked (e.g., error message or no login)
        assert "Too many login attempts. Please try again later." in self.driver.page_source  # Adjust based on your actual lockout message

        print("Account lockout test passed.")
        
        self.driver.close()
