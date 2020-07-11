from selenium import webdriver
import os
from time import sleep
GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'


def run(df, msg):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome('/path-to/chromedriver')
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    driver.get('https://web.whatsapp.com')
    sleep(5)

    numbers = df.values.tolist()

    data = {}

    for num in numbers:
        url = "https://web.whatsapp.com/send?phone=91" + str(num[1]) + "&text=" + "Hi " + num[0] + "! " + msg
        driver.get(url)
        sleep(3)
        for i in range(20):
            try:
                button = driver.find_element_by_xpath("//span[@data-icon='send']")
                button.click()
                driver.execute_script("window.onbeforeunload = function() {};")
                data[num[1]] = 1
                break
            except:
                print("not sent yet")
                data[num[1]] = 0
                sleep(1)
        print('Done ' + str(num[1]))

    driver.quit()
    return data
