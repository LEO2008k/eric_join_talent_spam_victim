import random
import string
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve settings from the configuration file
resume_path = config.get('settings', 'resume_path')
application_url = config.get('settings', 'application_url')
email_to_use = config.get('settings', 'email_to_use')

# Ensure the resume path is absolute
script_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.isabs(resume_path):
    resume_path = os.path.join(script_dir, resume_path)

# Function to generate random names with 1,000 characters
def generate_random_name(length=1000):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to clear a field
def clear_field(field):
    field.send_keys(Keys.COMMAND + "a")
    field.send_keys(Keys.DELETE)
    time.sleep(0.5)  # Ensure the field is cleared

# Function to fill out the form
def fill_form(driver):
    first_name = generate_random_name()
    last_name = generate_random_name()

    # Clicking on "Accept necessary only" button to dismiss popup
    try:
        accept_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonNecessary"))
        )
        accept_button.click()
        print("Clicked on 'Accept necessary only' button to dismiss popup.")
    except Exception as e:
        print("Error clicking on 'Accept necessary only' button:", e)

    # Delay after click
    time.sleep(1)

    # Wait for the form to load and fill out the fields
    try:
        print("Attempting to fill out first name field.")
        first_name_field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
        )
        clear_field(first_name_field)
        first_name_field.send_keys(first_name)
        print(f"Filled first name: {first_name}")

        print("Attempting to fill out last name field.")
        last_name_field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Last Name']"))
        )
        clear_field(last_name_field)
        last_name_field.send_keys(last_name)
        print(f"Filled last name: {last_name}")

        print("Attempting to fill out email field.")
        email_field = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))
        )
        clear_field(email_field)
        email_field.send_keys(email_to_use)
        print(f"Filled email: {email_to_use}")

        print("Attempting to click 'Please Upload Resume' button.")
        upload_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='upload-resume-button-jtn']"))
        )
        upload_button.click()
        print("Clicked 'Please Upload Resume' button.")
        
        print("Attempting to click 'Select file' button.")
        select_file_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-test-id='upload-resume-browse-button']"))
        )
        select_file_button.click()
        print("Clicked 'Select file' button.")
        
        # Delay after click to allow file input to appear
        time.sleep(1)

        print("Attempting to upload resume.")
        resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
        resume_input.send_keys(resume_path)
        print(f"Uploaded resume: {resume_path}")

        print("Attempting to click 'Agree' button.")
        agree_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='confirm-upload-resume']"))
        )
        agree_button.click()
        print("Clicked 'Agree' button.")

        # Clear and refill the fields after clicking "Agree"
        try:
            print("Attempting to clear and refill first name field.")
            first_name_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
            )
            clear_field(first_name_field)
            first_name_field.send_keys(first_name)
            print(f"Refilled first name: {first_name}")

            print("Attempting to clear and refill last name field.")
            last_name_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Last Name']"))
            )
            clear_field(last_name_field)
            last_name_field.send_keys(last_name)
            print(f"Refilled last name: {last_name}")

            print("Attempting to clear and refill email field.")
            email_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))
            )
            clear_field(email_field)
            email_field.send_keys(email_to_use)
            print(f"Refilled email: {email_to_use}")
        except Exception as e:
            print("Error clearing and refilling the fields:", e)
            print("Exception details:", e)

        # Check if the name already exists
        try:
            print("Checking if name already exists.")
            name_exists_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Name already exists')]"))
            )
            print("Name already exists. No further action taken.")
        except:
            # If the name does not exist, proceed with form submission
            print("Name does not exist. Proceeding with form submission.")

            print("Attempting to clear and refill first name field.")
            first_name_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
            )
            clear_field(first_name_field)
            first_name_field.send_keys(first_name)
            print(f"Refilled first name: {first_name}")

            print("Attempting to clear and refill last name field.")
            last_name_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Last Name']"))
            )
            clear_field(last_name_field)
            last_name_field.send_keys(last_name)
            print(f"Refilled last name: {last_name}")

            print("Attempting to clear and refill email field again.")
            email_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))
            )
            clear_field(email_field)
            email_field.send_keys(email_to_use)
            print(f"Refilled email again: {email_to_use}")

            print("Attempting to click privacy checkbox.")
            privacy_checkbox = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@data-test-id='careers-talent-network-privacy-checkbox-0']"))
            )
            privacy_checkbox.click()
            print("Clicked privacy checkbox.")

            print("Attempting to click newsletter checkbox.")
            newsletter_checkbox = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@aria-label='Yes, I would like to hear more about Ericsson and receive newsletters, invitations to events, congresses or other career related updates by email, text, or calls, to my contact details provided above.You may unsubscribe from the Talent Network or from subsequent communications at any time by contacting itm.external@ericsson.com or using the unsubscribe link in the respective communication.']"))
            )
            newsletter_checkbox.click()
            print("Clicked newsletter checkbox.")

            print("Attempting to click 'Join Talent Network' button.")
            submit_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='jtn-submit-btn']"))
            )
            submit_button.click()
            print("Clicked 'Join Talent Network' button.")

            # Wait for the server response (success message)
            try:
                print("Waiting for success message.")
                success_message = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Thanks For Joining Our Talent Network!')]"))
                )
                print("Thanks For Joining Our Talent Network!")
                sys.exit(0)
            except Exception as e:
                print("Failed to submit the form or the success message did not appear:", e)
                print("Exception details:", e)
                sys.exit(1)
    except Exception as e:
        print("Error filling out the form:", e)
        print("Exception details:", e)
        sys.exit(1)

# Function to open a browser session and fill out the form
def open_session():
    # Initialize Chrome options for Chrome Canary
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"  # Update this path if necessary
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36")

    # Create a new Chrome Canary session
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(application_url)  # Use the specified URL

    fill_form(driver)
    
    # Close the browser session after submission
    driver.quit()

# Open multiple browser sessions in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    for _ in range(3):
        executor.submit(open_session)

