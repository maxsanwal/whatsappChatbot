from .extract_chats import extract_chats
from .selenium_automation import automation
from .response import reply_message

def start_chat():
    sender = input("Give Sender Name(Keep it sames as in the file):")
    receiver = input("Give Your name(Keep in same as in the file):")
    chat_file_location = input("Enter filename: ")

    received_messages, sent_messages = extract_chats(sender, receiver, chat_file_location)
    input_box = automation(sender)
    reply_message(sender, sent_messages, input_box)




