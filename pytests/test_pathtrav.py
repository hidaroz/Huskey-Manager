import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestPathTraversal():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_path_traversal(self):
        base_url = "https://localhost/view_file.php?file="
        traversal_payloads = [
            "../../../../etc/passwd",  # Common file for UNIX systems
            "../../../../windows/win.ini",  # Common file for Windows systems
            "..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd"  # URL-encoded traversal
        ]
        
        for payload in traversal_payloads:
            self.driver.get(f"{base_url}{payload}")
            time.sleep(2)  # Adjust as needed for your application response time
            
            # Capture and log the page source to diagnose the response
            page_source = self.driver.page_source
            print(f"Response for Payload '{payload}':\n{page_source}\n")
            
            # Check for "File not found" to confirm that path traversal is blocked
            assert "File not found" in page_source or "404" in page_source
            
            # Optionally, check if other error messages are present
            # assert "Error" in page_source or "Forbidden" in page_source

        self.driver.close()
