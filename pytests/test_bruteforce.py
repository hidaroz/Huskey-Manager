import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestBruteForce():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_brute_force(self):
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)
        
        usernames = ["admin", "user", "test"]
        passwords = ["1234", "password", "admin123"]
        
        for username in usernames:
            for password in passwords:
                self.driver.find_element(By.ID, "username").click()
                self.driver.find_element(By.ID, "username").clear()
                self.driver.find_element(By.ID, "username").send_keys(username)
                
                self.driver.find_element(By.ID, "password").click()
                self.driver.find_element(By.ID, "password").clear()
                self.driver.find_element(By.ID, "password").send_keys(password)
                
                self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
                
                # Add an assertion or wait to check if the login attempt was successful
                time.sleep(1)  # Adjust as needed for your application response time
                # Example: Assert if login was successful (you'll need to adjust the following line based on actual application behavior)
                # assert "Welcome" in self.driver.page_source or another validation

                # Log or capture details of each attempt (optional)
                print(f"Attempted with Username: {username} and Password: {password}")

        self.driver.close()
