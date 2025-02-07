import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSuccessfulLogin:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Adjust implicit wait as necessary

    def teardown_method(self, method):
        self.driver.quit()

    def test_successful_login(self):
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)
        
        username = "username"  # Replace with a valid username
        correct_password = "Password!"  # Replace with a valid password
        
        # Fill in the login form
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(correct_password)
        
        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        time.sleep(1)  # Adjust as needed for your application response time
        
        # Assert that the login was successful by checking the URL or presence of a specific element
        assert "index.php" in self.driver.current_url or "Dashboard" in self.driver.page_source, "Login failed or Dashboard not found"
        
        print("Successful login test passed.")
