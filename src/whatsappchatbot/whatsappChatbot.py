from .extract_chats import extract_chats
from .selenium_automation import automation
from .response import reply_message
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def start_chat(sender, receiver, chat_file_location):
    received_messages, sent_messages = extract_chats(sender, receiver, chat_file_location)
    #'chromedriver/chromedriver'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://web.whatsapp.com")
    input("Scan the qr on whatsapp and press enter")

    input_box = automation(sender, driver)
    reply_message(sender, received_messages, sent_messages, input_box, driver)




