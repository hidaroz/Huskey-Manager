import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSessionTimeout:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_session_timeout(self):
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)

        username = "username"
        correct_password = "Password!"
        
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(correct_password)
        
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        
        # Ensure login was successful and redirected
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("index.php")  # Or any page you expect after login
        )

        # Simulate inactivity by setting a shorter sleep duration for testing
        time.sleep(5)  # Reduce this for testing purposes

        self.driver.get("https://localhost/logout.php")

        # Check if redirected to login page due to session timeout
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("login.php")
        )
        
        assert "login.php" in self.driver.current_url, "Not redirected to login page after session timeout"
        
        print("Session timeout test passed.")
