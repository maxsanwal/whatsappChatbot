from .extract_chats import extract_chats
from .selenium_automation import automation
from .response import reply_message
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def start_chat():
    sender = input("Give Sender Name(Keep it sames as in the file):")
    receiver = input("Give Your name(Keep in same as in the file):")
    chat_file_location = input("Enter filename: ")

    received_messages, sent_messages = extract_chats(sender, receiver, chat_file_location)
    #'chromedriver/chromedriver'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://web.whatsapp.com")
    input("Scan the qr on whatsapp and press enter")

    input_box = automation(sender, driver)
    reply_message(sender, received_messages, sent_messages, input_box, driver)




