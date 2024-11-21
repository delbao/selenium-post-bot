from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime
import logging
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from collections import defaultdict


# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the directory where media files are located
directory_path = "./media" # if this doesn't work use the one below and comment this one out
# directory_path = r"C:\Users\mathi\OneDrive\Dokumente\Business\Upwork Work\Jobs\Selenium-post-bot\media\\"

# List to store file information
file_list = []

class FacebookPoster:
    def __init__(self, driver_path='chromedriver'):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)

    def read_credentials(self, filepath='secrets.txt'):
        with open(filepath, 'r') as file:
            # Read the first line and split it into parts
            username, password = file.readline().split()
        return username, password

    def open_facebook(self, url='https://facebook.com'):
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(1.5)
        print("Webpage opened")

    def login(self):
        username, password = self.read_credentials()
        self.driver.find_element(By.NAME, 'email').send_keys(username)
        time.sleep(0.3)
        self.driver.find_element(By.NAME, 'pass').send_keys(password)
        time.sleep(0.3)
        self.driver.find_element(By.NAME, 'login').click()
        time.sleep(1)
        print("Logged in")

    def edit_post(self, text, file):
        """
        Edits a post on Facebook by adding the provided text/image to the post.
        """
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.HOME).perform()
            self.driver.get("https://www.facebook.com")
            logging.info("On the Homepage")
            create_post_area = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Create a post")]'))
            )
            logging.info("Create post area found")
            edit_text_element = create_post_area.find_element(By.XPATH, './/div[contains(@role, "button")]')
            edit_text_element.click()
            logging.info("Opened editor")


            self.add_text(text)

            if file:
                self.add_image(file["path"]) # adds an image to the post

            time.sleep(2)
            post_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Post"]'))
            )
            post_btn.click()
            time.sleep(5)
            logging.info("Post shared successfully")
            if file:
                self.edit_date(file["last_edit_day"], file["last_edit_time"])

        except Exception as e:
            logging.error(f"Failed to share the post: {e}")

    def add_text(self, text):
        logging.info("Adding text to the post")
        text_area = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[starts-with(@aria-label, "What\'s on your mind, ")]'))
        ) # find Text Box
        text_area.click()
        logging.info("Clicked on text area")
        text_area.send_keys(text) # Write text

    def add_image(self, file_path):
        """
        Adds image to the post. Needs the file path.
        """
        logging.info("Adding image to the post")
        add_media_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Photo/video']"))
        ) # find the Add Photo/video Button
        add_media_btn.click()
        logging.info("Image path: %s", file_path)
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form[@method='POST']//div//div//div//div//div//div//div//div//div//div//div//div//input[@type='file']"))
        ) # find the file input
        logging.info("File input found")
        file_input.send_keys(file_path) # send the path to the image

    def edit_date(self, file_date, file_time):
        """
        Edits the date of the last post. Needs date and time.
        """
        try:
            self.driver.get("https://www.facebook.com/profile.php") # go to own posts
            time.sleep(5) # possible fix for the crashing
            """
            try:
                last_post = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_RS"]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[1]'))
                ) # find last post
                logging.info("Found latest post")
            except  Exception as e:
                logging.error(f"Error finding latest post with data-pagelet attribute date: {e}")
                all_post = self.driver.find_element(By.XPATH, "//*[@data-pagelet='ProfileTimeline']")
                logging.info("Found all post")
                last_post = all_post[0]
                logging.info("Found latest post through relative XPath")
            """
            action_buttons = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//*[@aria-label='Actions for this post']"))
            )  # find last post
            logging.info("Found action button")
            action_buttons[0].click()
            logging.info("Clicked post action button")

            edit_option = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@role='menuitem']"))
            )[-3] # open the third option from the bottom
            logging.info("Found edit date option")
            edit_option.click()
            logging.info("Clicked edit date option")

            edit_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Edit Date']"))
            )
            logging.info("Found edit box")
            date_time = edit_box.find_elements(By.TAG_NAME, "input")
            logging.info("Found input boxes")
            date_time[0].send_keys(Keys.BACKSPACE * 20)  # clear Field
            date_time[0].send_keys(file_date) # write last modified day of file
            logging.info("Filled first box")
            date_time[1].send_keys(Keys.BACKSPACE * 20)  # clear Field
            date_time[1].send_keys(file_time) # write last modified time of file
            logging.info("Date and time edited")
            self.driver.find_element(By.XPATH, "//*[@aria-label='Done']").click() # click done
            logging.info("Clicked done")

        except Exception as e:
            logging.error(f"Error editing date: {e}")

    def close(self):
        self.driver.close()
        print("Browser closed")


def get_exif_date(image_path):
    """Extracts the EXIF date from an image file."""
    try:
        # Open image and extract EXIF data
        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data is not None:
            # Find the tag for DateTimeOriginal (which is the date the photo was taken)
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return value  # This will return the date in 'YYYY:MM:DD HH:MM:SS' format
        return None
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
        return None


def get_creation_date(file_path):
    """Gets the creation date of the file (from the file system)."""
    try:
        # Use os.path.getctime to get the file creation time (in seconds since the epoch)
        timestamp = os.path.getctime(file_path)
        # Convert timestamp to human-readable format
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"Error retrieving creation date: {e}")
        return None


def collect_file_info(dir_path):
    """
    Collects file information (path, last edited day and time, EXIF date if image) from the given directory.
    Uses EXIF date for images or file creation date as a fallback.
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if "C:" in dir_path:
                absolute_path = dir_path + file
            else:
                file_path = os.path.join(root, file)
                absolute_path = os.path.abspath(file_path)

            # Try to get the EXIF date if it's an image
            exif_date = None
            if file.lower().endswith(('jpg', 'jpeg', 'png')):
                exif_date = get_exif_date(absolute_path)

            # If EXIF date is not found, fallback to file creation date
            if exif_date:
                # EXIF date is in 'YYYY:MM:DD HH:MM:SS' format, so we need to convert it to a datetime object
                exif_datetime = datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
                # Format both day and time
                formatted_day = exif_datetime.strftime("%b %d, %Y")
                formatted_time = exif_datetime.strftime("%I:%M %p")
            else:
                # Get the creation date
                creation_date = get_creation_date(absolute_path)
                # Format both day and time
                formatted_day = creation_date.strftime("%b %d, %Y")
                formatted_time = creation_date.strftime("%I:%M %p")

            # Get file name without extension
            file_name_without_extension = Path(file).stem

            # Create a dictionary for each file with the absolute path, day, and time
            file_info = {
                "path": absolute_path,
                "last_edit_day": formatted_day,
                "last_edit_time": formatted_time,
                "file_name": file_name_without_extension
            }
            print(f"File found! File Name: {file_name_without_extension}, File Date: {formatted_day}, File Time: {formatted_time}, File Path: {absolute_path}")

            # Append to the list
            file_list.append(file_info)
    return file_list

# Main usage
if __name__ == "__main__":
    file_list = collect_file_info(directory_path)  # Collect file information
    fb_poster = FacebookPoster()
    fb_poster.open_facebook()
    fb_poster.login()
    time.sleep(10)
    if len(file_list) >= 1: # Check to see if there are files in the media folder. if not, just post the text.
        for file in file_list:
            logging.info("Working on %s; Date: %s; Time: %s", file["path"], file["last_edit_day"], file["last_edit_time"])
            fb_poster.edit_post("Hello, this is a test post!", file)
            time.sleep(5)
    else:
        fb_poster.edit_post("Hello, this is a test post!", "")

    time.sleep(5)
    fb_poster.close()