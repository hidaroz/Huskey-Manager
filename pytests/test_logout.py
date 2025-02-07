import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogout:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()  # Ensure you have the correct WebDriver
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_successful_logout(self):
        # Log in first to ensure that the user session is active
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)

        username = "username"  # Replace with a valid username
        correct_password = "Password!"  # Replace with a valid password
        
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(correct_password)
        
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        # Use WebDriverWait to wait for the login to complete
        WebDriverWait(self.driver, 10).until(
            EC.url_changes("https://localhost/login.php")
        )

        # Perform logout
        self.driver.get("https://localhost/logout.php")

        # Wait for redirection to complete
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("login.php")
        )

        # Check that the user is redirected to the login page
        assert "login.php" in self.driver.current_url, "Not redirected to login page after logout"
        
        print("Successful logout test passed.")
