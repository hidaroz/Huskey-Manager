import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSQLInjection():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_sql_injection(self):
        self.driver.get("https://localhost/login.php")
        self.driver.set_window_size(870, 1020)
        
        # Define SQL Injection payloads
        sql_payloads = [
            "' OR '1'='1",        # Classic SQL Injection payload
            "' OR '1'='1' --",    # Commenting out the rest of the query
            "' OR '1'='1' #",     # Another commenting style
            "' AND 1=CONVERT(int, (SELECT @@version)) --",  # Version extraction
            "' UNION SELECT NULL, NULL, NULL --"  # Union-based SQL Injection
        ]
        
        for payload in sql_payloads:
            # Test payload in the username field
            self.driver.find_element(By.ID, "username").click()
            self.driver.find_element(By.ID, "username").clear()
            self.driver.find_element(By.ID, "username").send_keys(payload)
            
            self.driver.find_element(By.ID, "password").click()
            self.driver.find_element(By.ID, "password").clear()
            self.driver.find_element(By.ID, "password").send_keys("dummy_password")
            
            self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
            time.sleep(2)  # Adjust as needed for your application response time
            
            # Capture and log the page source to diagnose the response
            page_source = self.driver.page_source
            print(f"Response for Payload '{payload}':\n{page_source}\n")
            
            # Check for different signs of injection success
            if "error" in page_source.lower() or "warning" in page_source.lower():
                print(f"Possible SQL Injection vulnerability detected with payload: {payload}")
            else:
                # Check for other signs of unexpected behavior
                assert "Login successful" not in page_source

        self.driver.close()
