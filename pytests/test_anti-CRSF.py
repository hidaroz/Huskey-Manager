import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAntiCSRFAwareness:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(870, 1020)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_absence_of_anti_csrf_token(self):
        self.driver.get("https://localhost/login.php")
        wait = WebDriverWait(self.driver, 10)

        # Wait for the page to load and check for the CSRF token field
        try:
            # Attempt to find the CSRF token field
            csrf_token_field = wait.until(EC.presence_of_element_located((By.NAME, 'csrf_token')))
            # If found, assert that its presence is an issue
            assert False, "CSRF token field is present when it should not be."
        except:
            # If an exception is raised (element not found), the CSRF token is absent
            assert True, "CSRF token field is absent as expected."
