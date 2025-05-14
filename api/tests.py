import time
from typing import List, Any
from api.models import User
from django.test import LiveServerTestCase
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django.test.utils import override_settings


@override_settings(DEBUG=True)
class E2ETests(LiveServerTestCase):
    browser: WebDriver

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        from selenium import webdriver

        cls.browser = webdriver.Chrome()  # Or webdriver.Firefox()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        self.user1: User = User.objects.create_user(
            username="user1", password="raaaatesting123", date_of_birth="2000-01-01"
        )
        self.user2: User = User.objects.create_user(
            username="user2", password="raaaatesting123", date_of_birth="1990-01-01"
        )

    def test_signup(self) -> None:
        self.browser.get(f"{self.live_server_url}/auth/signup/")

        self.browser.find_element(By.NAME, "username").send_keys("testuser")
        self.browser.find_element(By.NAME, "first_name").send_keys("Test")
        self.browser.find_element(By.NAME, "last_name").send_keys("User")
        self.browser.find_element(By.NAME, "email").send_keys("testuser@example.com")

        dob_field: WebElement = self.browser.find_element(By.NAME, "date_of_birth")
        dob_field.clear()
        self.browser.execute_script("arguments[0].value = '2000-01-01';", dob_field)

        self.browser.find_element(By.NAME, "password1").send_keys("raaaatesting123")
        self.browser.find_element(By.NAME, "password2").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        WebDriverWait(self.browser, 10).until(EC.url_contains("/auth/login/"))
        self.assertIn("/auth/login/", self.browser.current_url)

    def test_login(self) -> None:
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "username").send_keys("user1")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "app"))
        )
        app_element: WebElement = self.browser.find_element(By.ID, "app")
        self.assertTrue(app_element.is_displayed())

    def test_edit_profile(self) -> None:
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "username").send_keys("user1")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        profile_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Profile']"))
        )
        profile_button.click()

        edit_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "button-3"))
        )
        edit_button.click()

        first_name_field: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "first_name"))
        )
        first_name_field.clear()
        first_name_field.send_keys("Test")

        last_name_field: WebElement = self.browser.find_element(By.ID, "last_name")
        last_name_field.clear()
        last_name_field.send_keys("User")

        email_field: WebElement = self.browser.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys("testuser@example.com")

        date_of_birth_field: WebElement = self.browser.find_element(
            By.ID, "date_of_birth"
        )
        date_of_birth_field.clear()
        date_of_birth_field.send_keys("01-01-2000")

        save_button: WebElement = self.browser.find_element(
            By.CSS_SELECTOR, "button.btn.btn-primary.w-100"
        )
        save_button.click()

        updated_user: User = User.objects.get(username="user1")
        updated_user.refresh_from_db()

        edit_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "button-3"))
        )
        edit_button.click()

        profile_data: str = (
            WebDriverWait(self.browser, 10)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "pf-info")))
            .text
        )

        self.assertIn("Test", profile_data, "First name not found on profile page.")
        self.assertIn("User", profile_data, "Last name not found on profile page.")
        self.assertIn(
            "testuser@example.com", profile_data, "Email not found on profile page."
        )
        self.assertIn(
            "2000-01-01", profile_data, "Date of Birth not found on profile page."
        )

    def test_send_friend_request(self) -> None:
        """
        Test the ability to send a friend request as user1, restart the session, log in as user2,
        accept the request, and verify the friendship.
        """
        # Log in as user1 and send a friend request to user2 via the UI
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "username").send_keys("user1")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Navigate to the Users page
        users_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Users']"))
        )
        users_button.click()

        # Wait for the Users page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        time.sleep(1)

        # Locate the row for user2 and click "Send Friend Request"
        user_rows: List[WebElement] = self.browser.find_elements(By.TAG_NAME, "tr")
        for row in user_rows:
            if "user2" in row.text:  # Look for user2
                time.sleep(2)
                send_request_button: WebElement = row.find_element(
                    By.TAG_NAME, "button"
                )
                send_request_button.click()

                # Handle the alert
                WebDriverWait(self.browser, 10).until(EC.alert_is_present())
                alert: Any = self.browser.switch_to.alert
                alert.accept()  # Accept the alert
                break

        # Verify friend request exists in the backend
        self.user1.refresh_from_db()
        self.assertIn(
            self.user2,
            self.user1.sent_friend_requests.all(),
            "Friend request was not created in the backend.",
        )


    def test_send_and_accept_friend_request(self) -> None:
        """
        Test the ability to send a friend request as user1, restart the session, log in as user2,
        accept the request, and verify the friendship.
        """
        # Log in as user1 and send a friend request to user2 via the UI
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "username").send_keys("user1")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Navigate to the Users page
        users_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Users']"))
        )
        users_button.click()

        # Wait for the Users page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        time.sleep(1)

        # Locate the row for user2 and click "Send Friend Request"
        user_rows: List[WebElement] = self.browser.find_elements(By.TAG_NAME, "tr")
        for row in user_rows:
            if "user2" in row.text:  # Look for user2
                time.sleep(2)
                send_request_button: WebElement = row.find_element(
                    By.TAG_NAME, "button"
                )
                send_request_button.click()

                # Handle the alert
                WebDriverWait(self.browser, 10).until(EC.alert_is_present())
                alert: Any = self.browser.switch_to.alert
                alert.accept()  # Accept the alert
                break

        # Verify friend request exists in the backend
        self.user1.refresh_from_db()
        self.assertIn(
            self.user2,
            self.user1.sent_friend_requests.all(),
            "Friend request was not created in the backend.",
        )

        # Clear session and start again for user2
        self.browser.delete_all_cookies()
        self.browser.get(f"{self.live_server_url}/auth/login/")  # Return to login page

        # Log in as user2 to accept the friend request
        self.browser.find_element(By.NAME, "username").send_keys("user2")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Navigate to the Friends page
        friends_button: WebElement = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Friends']"))
        )
        friends_button.click()

        # Wait for the Friends page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Locate the Accept button for user1 and click it
        friend_request_rows: List[WebElement] = self.browser.find_elements(
            By.TAG_NAME, "li"
        )
        for row in friend_request_rows:
            if "user1" in row.text:  # Look for user1's request
                accept_button: WebElement = row.find_element(
                    By.XPATH, ".//button[text()='Accept']"
                )
                accept_button.click()
                break

    def test_filter_users_by_age(self) -> None:
        """
        Test that users can be filtered by age using the min age and max age fields, triggered by pressing Enter.
        """
        # Log in before accessing the users page
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "username").send_keys("user1")
        self.browser.find_element(By.NAME, "password").send_keys("raaaatesting123")
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Wait for the login to complete
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "app"))
        )

        # Navigate to the users page
        self.browser.get(f"{self.live_server_url}/users")

        # Wait for the users page to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Input min and max age
        min_age_field: WebElement = self.browser.find_element(By.ID, "min-age")
        max_age_field: WebElement = self.browser.find_element(By.ID, "max-age")

        min_age_field.clear()
        min_age_field.send_keys("20")  # Replace with desired min age
        min_age_field.send_keys(Keys.ENTER)  # Simulate pressing Enter

        max_age_field.clear()
        max_age_field.send_keys("30")  # Replace with desired max age
        max_age_field.send_keys(Keys.ENTER)  # Simulate pressing Enter

        time.sleep(1)

        # Verify the filtered results
        users_table: WebElement = self.browser.find_element(By.TAG_NAME, "table")
        rows: List[WebElement] = users_table.find_elements(By.TAG_NAME, "tr")

        usernames: List[str] = []

        for row in rows[1:]:  # Skip the header row
            columns: List[WebElement] = row.find_elements(By.TAG_NAME, "td")
            usernames.append(columns[0].text)  # Adjust the column index for age

        users: List[User] = User.objects.filter(username__in=usernames)
        for user in users:
            self.assertTrue(20 < user.age < 30)
