from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FacebookPoster:
    def __init__(self, driver_path='chromedriver'):
        self.driver = webdriver.Chrome()
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

    def share_post(self, text, photo_url=None):
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.HOME).perform()

            create_post_area = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Create a post")]')
            edit_text_element = create_post_area.find_element(By.XPATH, './/div[contains(@role, "button")]')
            edit_text_element.click()

            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="What\'s on your mind, Del?"]'))
            )

            post_form = self.driver.find_element(By.TAG_NAME, 'form')
            text_area = post_form.find_element(By.XPATH, '//div[@aria-label="What\'s on your mind, Del?"]')
            text_area.click()
            text_area.send_keys(text)

            post_btn = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Post"]')
            post_btn.click()

            print("Post Shared Successfully")
        except Exception as e:
            print("Failed to share the post", e)

    def close(self):
        self.driver.close()
        print("Browser closed")

# Main usage
if __name__ == "__main__":
    fb_poster = FacebookPoster()
    fb_poster.open_facebook()
    fb_poster.login()
    time.sleep(10)
    fb_poster.share_post("Hello, this is a test post!")
    fb_poster.close()
