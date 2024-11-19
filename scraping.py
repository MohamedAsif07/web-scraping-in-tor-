#!/usr/bin/env python3

from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from PIL import Image
import pytesseract
import numpy as np
import cv2
import logging
import time
import threading  # Import threading for animation

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your CAPTCHA solving settings
TESSERACT_CMD = '/usr/bin/tesseract'  # Path to Tesseract executable
CAPTCHA_RETRY_LIMIT = 3
CAPTCHA_WAIT_TIME = 30  # Time to wait between CAPTCHA solution attempts
TOR_CONTROL_PASSWORD = "your_tor_pass"  # Replace with your actual Tor control password
USERNAME = "onion_username"  # Your username
PASSWORD = "onion_password"  # Your password

# Function to connect to the Tor control port and refresh the IP
def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=TOR_CONTROL_PASSWORD)
            controller.signal(Signal.NEWNYM)
        logging.info("IP address renewed through Tor.")
    except Exception as e:
        logging.error(f"Failed to renew Tor IP: {e}")

# Function to initiate Selenium browser through Tor
def start_selenium_with_tor():
    options = Options()
    options.headless = False  # Set to True to run without GUI
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9050)
    options.set_preference('network.proxy.socks_version', 5)
    options.set_preference('network.proxy.socks_remote_dns', True)

    logging.info("Starting Selenium with these proxy settings.")
    driver = webdriver.Firefox(options=options)
    return driver

# Function to preprocess CAPTCHA image for better OCR
def preprocess_captcha(captcha_image):
    gray_image = cv2.cvtColor(np.array(captcha_image), cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((1, 1), np.uint8)
    cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    return cleaned_image

# Function to solve CAPTCHA using Tesseract OCR
def solve_captcha(captcha_img_path):
    for attempt in range(CAPTCHA_RETRY_LIMIT):
        try:
            captcha_image = Image.open(captcha_img_path)
            preprocessed_image = preprocess_captcha(captcha_image)
            preprocessed_img_path = "preprocessed_captcha.png"
            cv2.imwrite(preprocessed_img_path, preprocessed_image)
            logging.info(f"Preprocessed CAPTCHA image saved: {preprocessed_img_path}")

            pil_image = Image.fromarray(preprocessed_image)
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
            
            captcha_text = pytesseract.image_to_string(pil_image, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz').strip()

            if captcha_text:
                logging.info(f"CAPTCHA text extracted: {captcha_text}")
                return captcha_text
            else:
                logging.warning("Failed to extract text from CAPTCHA.")
        except Exception as e:
            logging.error(f"Error during CAPTCHA processing: {e}")

        time.sleep(CAPTCHA_WAIT_TIME)  # Wait before retrying

    return None

# Function to log in, including CAPTCHA handling
def login_onion_site(driver):
    try:
        driver.get("replace your onnion link") # replace your onion link

        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        # Extract CSRF token
        csrf_token = driver.find_element(By.NAME, 'my_post_key').get_attribute('value')
        logging.info(f"CSRF Token: {csrf_token}")

        # Wait for CAPTCHA to load and capture a screenshot for debugging
        captcha_img_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'captcha_img')))
        captcha_img_path = "captcha_image_selenium.png"
        captcha_img_element.screenshot(captcha_img_path)
        logging.info(f"CAPTCHA image saved via Selenium: {captcha_img_path}")

        # Solve the CAPTCHA locally
        captcha_solution = solve_captcha(captcha_img_path)
        if captcha_solution:
            logging.info(f"CAPTCHA Solution: {captcha_solution}")
            captcha_input = driver.find_element(By.NAME, 'imagestring')
            captcha_input.send_keys(captcha_solution)

            # Set the hidden fields before submission
            driver.execute_script("document.getElementsByName('my_post_key')[0].value = arguments[0];", csrf_token)
            driver.execute_script("document.getElementsByName('action')[0].value = 'do_login';")

            # Scroll to the submit button
            submit_button = driver.find_element(By.NAME, 'submit')
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)  # Optional: wait a moment after scrolling

            # Click the button directly using JavaScript
            driver.execute_script("arguments[0].click();", submit_button)

            WebDriverWait(driver, 15).until(EC.title_contains("Login Successful"))  # Adjust based on expected title

            logging.info("Login successful.")
            return driver.get_cookies()
        else:
            logging.warning("CAPTCHA solution failed.")
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return None

# Function to scrape page content post-login using Requests
def scrape_after_login(session, cookies):
    try:
        url = ""   # replace your onion link

        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050',
        }

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        response = session.get(url)
        logging.info("Page content retrieved after login.")
        print(response.text)

    except Exception as e:
        logging.error(f"Error scraping after login: {e}")

def loading_animation():   # developer darkstrom
    loading_text = "Dark strom "
    logo = """
    
      ____    _    ____  _  __  ____ _____ ____   ___  __  __   __________ 
     |  _ \  / \  |  _ \| |/ / / ___|_   _|  _ \ / _ \|  \/  | |___ /___ / 
     | | | |/ _ \ | |_) | ' /  \___ \ | | | |_) | | | | |\/| |   |_ \ |_ \ 
     | |_| / ___ \|  _ <| . \   ___) || | |  _ <| |_| | |  | |  ___) |__) |
     |____/_/   \_\_| \_\_|\_\ |____/ |_| |_| \_\\___/|_|  |_| |____/____/ 


     
    """
    
    print(logo)  
    while not stop_loading_event.is_set():
        for i in range(4):  # Length of the loading animation
            print(f"\r{loading_text}{'.' * i}", end="")
            time.sleep(0.5)
    print("\rLoading completed!  ")  
    
    
# Main program flow
if __name__ == "__main__":
    driver = None
    stop_loading_event = threading.Event()  # Event to stop the loading animation

    # Start the loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    try:
        renew_tor_ip()
        driver = start_selenium_with_tor()
        cookies = login_onion_site(driver)

        if cookies:
            session = requests.Session()
            scrape_after_login(session, cookies)
        else:
            logging.warning("Login failed or CAPTCHA not solved.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        stop_loading_event.set()  # Stop the loading animation
        loading_thread.join()  # Wait for the loading thread to finish
        if driver:
            driver.quit()
