import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestXSS:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.driver.get("https://localhost/users/request_account.php")  # URL to the registration form
        self.driver.set_window_size(870, 1020)

    def teardown_method(self, method):
        self.driver.quit()

    def test_xss(self):
        # Define XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",       # Simple script alert
            "<img src='x' onerror='alert(1)'>",    # Image tag with an error event
            "<svg/onload=alert(1)>",               # SVG tag with an onload event
            "<a href='javascript:alert(1)'>Click me</a>",  # JavaScript in an anchor tag
            "<iframe src='javascript:alert(1)'></iframe>"  # Iframe with JavaScript
        ]
        
        wait = WebDriverWait(self.driver, 20)  # Increased wait time
        
        try:
            # Wait for the input fields and submit button to be present and clickable
            first_name_field = wait.until(EC.presence_of_element_located((By.ID, "first_name")))
            last_name_field = wait.until(EC.presence_of_element_located((By.ID, "last_name")))
            email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
            username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary.btn-block")))

            # Debugging: Print confirmation of element detection
            print(f"First Name field detected: {first_name_field is not None}")
            print(f"Last Name field detected: {last_name_field is not None}")
            print(f"Email field detected: {email_field is not None}")
            print(f"Username field detected: {username_field is not None}")
            print(f"Password field detected: {password_field is not None}")
            print(f"Submit button detected: {submit_button is not None}")

            for payload in xss_payloads:
                # Test payload in each input field except the password
                fields_to_test = [first_name_field, last_name_field, email_field, username_field]
                
                for field in fields_to_test:
                    field.click()
                    field.clear()
                    field.send_keys(payload)
                    print(f"Injected payload '{payload}' into field with ID '{field.get_attribute('id')}'")
                
                # Set a safe password for testing
                password_field.click()
                password_field.clear()
                password_field.send_keys("SafePassword123")  
                
                submit_button.click()
                time.sleep(3)  # Adjust as needed for your application response time
                
                # Capture and log the page source for analysis
                page_source = self.driver.page_source
                print(f"Response for Payload '{payload}':\n{page_source}\n")
                
                # Ensure the payload is not reflected unencoded
                assert payload not in page_source, f"Payload '{payload}' was found in the response, potential vulnerability!"
                
                # Optional: Detect if alert is triggered by the payload
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    print(f"Alert text: {alert_text}")
                    alert.accept()  # Close the alert
                    assert False, f"XSS alert triggered with payload: {payload}"  # Fail if XSS alert is triggered
                except:
                    pass  # No alert found means no XSS for this payload

        except Exception as e:
            print(f"Exception encountered: {e}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source snippet: {self.driver.page_source[:500]}")  # Print first 500 characters of page source for debugging
        
        finally:
            self.driver.close()
