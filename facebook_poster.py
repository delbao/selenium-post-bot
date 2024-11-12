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

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the directory where media files are located
directory_path = "./media"

# List to store file information
file_list = []

# Index of the file to process
file_number = 0

class FacebookPoster:
    def __init__(self, driver_path='chromedriver'):
        self.driver = webdriver.Chrome()

        # self.driver.implicitly_wait(5)

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

    def edit_post(self, text, post_image):
        """
        Edits a post on Facebook by adding the provided text/image to the post.
        """
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.HOME).perform()

            create_post_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Create a post")]'))
            )
            edit_text_element = create_post_area.find_element(By.XPATH, './/div[contains(@role, "button")]')
            edit_text_element.click()
            logging.info("Opened editor")


            self.add_text(text)

            if post_image:
                self.add_image()

            time.sleep(2)
            post_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Post"]'))
            )
            post_btn.click()
            time.sleep(5)
            logging.info("Post shared successfully")
            if post_image:
                self.edit_date()

        except Exception as e:
            logging.error(f"Failed to share the post: {e}")

    def add_text(self, text):
        logging.info("Adding text to the post")
        text_area = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        ) # find Text Box
        text_area.click()
        logging.info("Clicked on text area")
        text_area.send_keys(text) # Write text

    def add_image(self):
        logging.info("Adding image to the post")
        add_media_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Photo/video']"))
        ) # find the Add Photo/video Button
        add_media_btn.click()

        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/input"))
        ) # find the file input (only full xpath seems to work)
        logging.info("File input found")
        file_input.send_keys(file_list[file_number]["path"]) # send the path to the image
        return True

    def edit_date(self):
        """
        Edits the date of the last post.
        """
        try:
            self.driver.get("https://www.facebook.com/profile.php") # go to own posts
            own_post = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@data-pagelet='TimelineFeedUnit_0']"))
            ) # find last post
            own_post.find_element(By.XPATH, "//*[@aria-label='Actions for this post']").click()
            logging.info("Clicked post action button")

            edit_option = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@role='menuitem']"))
            )[-3] # open the third option from the bottom
            edit_option.click()
            logging.info("Clicked edit date option")

            edit_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Edit Date']"))
            )
            date_time = edit_box.find_elements(By.TAG_NAME, "input")
            date_time[0].send_keys(Keys.BACKSPACE * 20)  # clear Field
            date_time[0].send_keys(file_list[file_number]["last_edit_day"]) # write last modified day of file
            date_time[1].send_keys(Keys.BACKSPACE * 20)  # clear Field
            date_time[1].send_keys(file_list[file_number]["last_edit_time"]) # write last modified time of file
            logging.info("Date and time edited")
            self.driver.find_element(By.XPATH, "//*[@aria-label='Done']").click() # click done

        except Exception as e:
            logging.error(f"Error editing date: {e}")

    def close(self):
        self.driver.close()
        print("Browser closed")

def collect_file_info(directory_path):
    """
    Collects file information (path, last modified day and time) from the given directory.
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Combine the root directory and file name to get the file path
            file_path = os.path.join(root, file)

            # Convert the relative file path to an absolute path
            absolute_path = os.path.abspath(file_path)

            # Get the last modification time and convert it to a readable format
            last_edit_date = datetime.fromtimestamp(os.path.getmtime(absolute_path))

            # Format the last edit date
            formatted_day = last_edit_date.strftime("%b %d, %Y")  # Format for day (e.g., Nov 10, 2024)
            formatted_time = last_edit_date.strftime("%I:%M %p")  # Format for time (e.g., 8:15 PM)

            # Create a dictionary for each file with the absolute path, day, and time
            file_info = {
                "path": absolute_path,
                "last_edit_day": formatted_day,
                "last_edit_time": formatted_time
            }

            # Append to the list
            file_list.append(file_info)
    return file_list

# Main usage
if __name__ == "__main__":
    file_list = collect_file_info(directory_path)  # Collect file information

    # image prompt in console
    image = int(input("Do you want to add an image? 1 for yes; 0 for no: "))
    if image:
        for file in file_list:
            print(file["path"])
        file_number = int(input("What file do you want to add? Beginning from 0: "))

    fb_poster = FacebookPoster()
    fb_poster.open_facebook()
    fb_poster.login()
    time.sleep(10)
    fb_poster.edit_post("Hello, this is a test post!", image)
    time.sleep(5)
    fb_poster.close()