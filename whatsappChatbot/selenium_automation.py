from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def automation(sender_name):
    print('To find')
    driver = webdriver.Chrome('chromedriver/chromedriver')
    print('Found')
    driver.get("https://web.whatsapp.com")
    input("Scan the qr on whatsapp and press enter")

    #to find and open a specific contact
    x_arg = "//span[@title='{}']"
    user = driver.find_element_by_xpath(x_arg.format(sender_name))
    user.click()

    #to select the text box
    inp_xpath = '//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="6"]'
    input_box = driver.find_element_by_xpath(inp_xpath)

    return input_box
    
