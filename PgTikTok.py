import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException


class TikTokClass:

    def get_info_from_script(self):

        # Get the file path for script
        file_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop",
            "Daily_accounts",
            "bread_fall_daily",
            "Script_bread_fall_daily_youtube.txt",
        )

        info_dict = {}
        try:
            with open(file_path, "r") as file:
                current_key = None
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespace

                    if ":" in line:
                        current_key, value = line.strip().split(":", 1)
                        info_dict[current_key.strip()] = value.strip()
                    else:
                        # Append to description if same key
                        if current_key == "Description":
                            info_dict[current_key] += "\n" + line
                        else:
                            # Handle unexpected line format (optional)
                            print(f"Warning: Unexpected line format: {line}")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")

        return info_dict

    # Extracts the month and day from a string date in format "MM/DD/YYYY".
    def extract_month_day(self, string_date):
        try:
            # Split the string date into components using "/" as delimiter
            month, day, year = string_date.split("/")

            # Convert month string to full month name (optional)
            month_names = {
                "01": "January",
                "02": "February",
                "03": "March",
                "04": "April",
                "05": "May",
                "06": "June",
                "07": "July",
                "08": "August",
                "09": "September",
                "10": "October",
                "11": "November",
                "12": "December",
            }
            month = month_names.get(
                month, month
            )  # Use original month string if not found in dictionary

            # Convert day string to integer
            day = int(day)

            return month, day
        except ValueError:
            # Handle invalid date format
            print("Invalid date format. Please use MM/DD/YYYY.")
            return None, None

    # Function to find and click on the specified day number
    def find_and_click_day(self, driver, day_number):
        # Wait for the calendar days to be present
        days_of_the_month = driver.find_elements("span.day")

        # Find the index of the day with text "1"
        start_index = None
        for index, day in enumerate(days_of_the_month):
            if day.text == "1":
                start_index = index
                break

        # If "1" is found, traverse the calendar starting from the next day
        if start_index is not None:
            for day in days_of_the_month[start_index:]:
                if day.text == str(day_number):
                    day.click()
                    print(f"Clicked on day {day_number}")
                    break
        else:
            print("The calendar does not contain day 1")

    # Parses a time string in the format "HH:MM" and returns a tuple of (hour, minute).
    # Args:time_string: The time string to parse (e.g., "8:00", "16:55").
    # Returns: A tuple of (hour, minute) integers, or None if the format is invalid.
    # Raises: ValueError: If the time string is in an invalid format.
    def parse_time_string(self, time_string):
        try:
            # Split the string by colon (':') to separate hours and minutes
            hour, minute = time_string.split(":")

            # Convert hour and minute strings to integers
            hour = int(hour)
            minute = int(minute)

            # Validate the parsed values (0-23 for hour, 0-59 for minute)
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return hour, minute
            else:
                raise ValueError(
                    "Invalid time format. Hour must be between 0 and 23, minute between 0 and 59."
                )
        except ValueError as e:
            print(f"Error parsing time string: {e}")
            return None

    def select_time_from_dropdown(self, driver, time_scrollbar_element, time_string):

        # cursor hove over time_scrollbar_elements[0]
        actions = ActionChains(driver)
        actions.move_to_element(time_scrollbar_element).perform()

        # Scroll up loop
        initial_scroll_position = int(
            driver.execute_script(
                "return arguments[0].scrollTop", time_scrollbar_element
            )
        )

        # Scroll up loop
        for i in range(initial_scroll_position, 0, -100):

            driver.execute_script(
                "arguments[0].scrollTop -= 100", time_scrollbar_element
            )
            # driver.sleep(0.01)  # Adjust the sleep time to control the scrolling speed
            try:
                # Check if the desired option is present
                options = time_scrollbar_element.find_elements(
                    By.CSS_SELECTOR, "div.tiktok-timepicker-option-item"
                )
                if options:
                    wait = WebDriverWait(driver, 0)  # Set a timeout of 1 second
                    wait.until(EC.element_to_be_clickable(options[time_string]))
                    options[time_string].click()
                    break
            except:
                # If the option is not found, continue scrolling
                continue

        scroll_height = driver.execute_script(
            "return arguments[0].scrollHeight", time_scrollbar_element
        )

        # Scroll down loop
        for i in range(0, scroll_height, 100):
            driver.execute_script(
                "arguments[0].scrollTop += 100", time_scrollbar_element
            )
            # driver.sleep(0.01)  # Adjust the sleep time to control the scrolling speed
            try:
                # Check if the desired option is present
                options = time_scrollbar_element.find_elements(
                    By.CSS_SELECTOR, "div.tiktok-timepicker-option-item"
                )
                if options:
                    wait = WebDriverWait(driver, 0)  # Set a timeout of 1 second
                    wait.until(EC.element_to_be_clickable(options[time_string]))
                    options[time_string].click()
                    break
            except:
                # If the option is not found, continue scrolling
                continue

    def login_to_tiktok(self, driver):

        # Retrieve information from the file
        info = self.get_info_from_script()

        # access to tiktok login page
        driver.get("https://www.tiktok.com/login/phone-or-email/email")

        # enter username
        username = driver.wait_for_element('[name="username"]')
        username.clear()
        username.send_keys(info["Email"])

        # enter password
        password = driver.wait_for_element('[type="password"]')
        password.clear()
        password.send_keys(info["Password"])

        # clicks on submit
        driver.wait_for_element('[type="submit"]').click()

        # driver will wait until user resolve captcha
        driver.implicitly_wait(300)  # Wait for up to 300 seconds for any element

    def automate_content_planner(self, driver):

        # Retrieve information from the file
        info = self.get_info_from_script()

        # Now try to find and click the element (might fail initially but wait for up to 30 seconds)
        try:
            target_element = driver.find_element(
                By.CSS_SELECTOR, "span.css-y3rt08-SpanUploadText.e18d3d946"
            )
            target_element.click()
            print("Element found and clicked!")
        except:
            print("Element not found within the timeout period.")

        # Execute JavaScript to count iframes
        iframe_count = driver.execute_script(
            "return document.getElementsByTagName('iframe').length;"
        )

        if iframe_count > 0:
            iframe_element = driver.find_element(
                By.CSS_SELECTOR, "iframe[data-tt='Upload_index_iframe']"
            )  # Replace with actual ID or other locator

            # Switch focus to the iframe (important!)
            driver.switch_to.frame(iframe_element)
        else:
            print("There is no iframe")

        # Get the file path for video
        file_path = os.path.join(os.path.expanduser("~"), info["Data_path"])

        # Convert the starting date string to a datetime object
        start_date = datetime.strptime(info["Start_date"], "%m/%d/%Y")

        for i in range(int(info["Last_day_uploaded"]), int(info["Upload_until_day"])):

            # uploads video
            input_field = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            input_field.send_keys(file_path)

            # waits for the element related to the upload progress percentage
            driver.wait_for_element("div.info-progress-num")

            # Wait for the text to be "100%"
            try:
                WebDriverWait(driver, 20).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "div.info-progress-num"), "100%"
                    )
                )
                print("Progress reached 100%")
            except TimeoutException:
                print("Progress did not reach 100% within 20 seconds.")

            # locates the element for the description of the video
            driver.wait_for_element("div.caption-wrap-v2").click()

            # we need to use actions so we can write the description of the video
            actions = ActionChains(driver)
            actions.key_down(Keys.COMMAND).send_keys("a").key_up(Keys.COMMAND).perform()
            actions.send_keys(
                f"Day {i+1} " + info["Description"]
            ).perform()  # description of the video
            driver.sleep(2)

            # clicks on "schedule" checkbox
            driver.wait_for_element('[value="schedule"]').click()

            # Locate all elements with the class "tiktok-timepicker-disable-scrollbar"
            time_scrollbar_elements = driver.find_elements(
                "div.tiktok-timepicker-disable-scrollbar"
            )

            # stores the date and time drop down list locators
            time_and_date_lists = driver.find_elements("input.TUXTextInputCore-input")

            # Stores the hour and minute from Script Time
            time_string = info["Time"]
            hour, minute = self.parse_time_string(time_string)
            minute = int(minute / 5)

            if hour is not None and minute is not None:
                print(f"Hour: {hour}, Minute: {minute}")
            else:
                print("Invalid time string format.")

            # clicks on "time" dropdown list
            time_and_date_lists[0].click()

            # Selects the hour from the dropdown list
            self.select_time_from_dropdown(driver, time_scrollbar_elements[0], hour)

            driver.sleep(2)

            # clicks on "time" dropdown list
            time_and_date_lists[0].click()

            # Selects the minute from the dropdown list
            self.select_time_from_dropdown(driver, time_scrollbar_elements[1], minute)

            driver.sleep(2)

            # clicks on "date" dropdown list
            time_and_date_lists[1].click()

            # Add i days to the starting date
            current_date = start_date + timedelta(days=i)
            # Format the date as desired (e.g., MM/DD/YYYY)
            formatted_date = current_date.strftime("%m/%d/%Y")

            # Get the month and the day from date String
            month, day = self.extract_month_day(formatted_date)

            while True:
                # Wait for the month header element to be present
                month_header_element = driver.wait_for_element(
                    "div.month-header-wrapper"
                )

                # Get the text of the month header element
                month_text = month_header_element.text
                print(f"Month header text: {month_text}")

                # Check if the month text is correct
                if month in month_text:
                    print("Month found!")
                    break

                # Wait for the arrow elements to be present
                arrow_elements = driver.find_elements("span.arrow")
                # Click the second arrow (right arrow)
                arrow_elements[1].click()

            # Clicks on the day on pop up calendar
            self.find_and_click_day(driver, day)
            driver.sleep(2)

            # clicks on "schedule" buttton
            driver.wait_for_element("button.TUXButton--primary").click()

            # clicks on "Upload Another Video" buttton
            driver.wait_for_element(
                "button.TUXButton--medium.TUXButton--primary"
            ).click()
