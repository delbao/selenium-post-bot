# import all libraries
from selenium import webdriver as web
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# get driver from main page
def drivers(driv):
    global driver
    driver = driv

# open url and max window


def openurl(url):
    driver.get(url)
    driver.maximize_window()
    time.sleep(1.5)
    print("Webpage opened")

# login webpage


def login(usrn, passw):
    # write username
    driver.find_element(By.NAME, 'email').send_keys(usrn)
    time.sleep(0.3)

    # write password
    driver.find_element(By.NAME, 'pass').send_keys(passw)
    time.sleep(0.3)

    # click login button
    driver.find_element(By.NAME, 'login').click()
    time.sleep(1)
    print("Logged in")

# share post (with pic or without)

# def share_post(text, photo_url="None"):
#     print("Start Sharing")
#
#     #share post button click
#     driver.find_element(By.XPATH, "//h3[text()='Create a post']").click()
#     time.sleep(20)
#
#     #if you choose photo+text mode active this section
#     if photo_url != "None":
#         #open drop img section
#         driver.find_element(By.XPATH, "//div[contains(text(), 'Photo/Video')]").click()
#         time.sleep(1)
#
#         #upload img
#         driver.find_element(By.XPATH, "//input[@accept='image/*']").send_keys(photo_url)
#         time.sleep(2)
#
#     #write text
#     driver.find_element(By.XPATH, "//div[@role='textbox']").send_keys(text)
#     time.sleep(1)
#
#     #click share button
#     driver.find_element(By.XPATH, "//div[contains(text(), 'Post')]").click()
#
#     print("Post Shared")


def share_post(text, photo_url="None"):
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.HOME).perform()

        create_post_area = driver.find_element(
            By.XPATH, '//div[contains(@aria-label, "Create a post")]')
        edit_text_element = create_post_area.find_element(
            By.XPATH, './/div[contains(@role, "button")]')
        edit_text_element.click()

        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@aria-label="What\'s on your mind, Del?"]')
            )
        )

        # Not working 1: text_area = driver.find_element(
        #     By.XPATH, '//div[contains(@aria-describedby, "placeholder")]')
        # Not working 2:
        # text_area = driver.find_element(By.XPATH, '//div[contains(@role, "textbox")]')
        # Not working 3: text_area = driver.find_element(By.XPATH,  "//textarea[@aria-label=\"What's on your mind?\"]")
        post_form = driver.find_element(By.TAG_NAME, 'form')
        text_area = post_form.find_element(
            By.XPATH, '//div[@aria-label="What\'s on your mind, Del?"]')
        text_area.click()
        text_area.send_keys(text)

        post_btn = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Post"]')
        post_btn.click()

        # WebDriverWait(driver, 10).until(
        #     EC.invisibility_of_element_located(
        #         (By.CSS_SELECTOR, 'div[aria-label="Post"]'))
        # )

        print("Post Shared Successfully")
    except Exception as e:
        print("Failed to share the post", e)
