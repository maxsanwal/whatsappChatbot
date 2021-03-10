import re

#seperating chats into list of 2 users
def extract_chats(sender_name, receiver_name):
    #reading the chats into a string
    chat_filename = input("Enter filename: ")
    f = open(chat_filename, encoding="utf8")
    chat_string = f.read()
    re_date_time = '\d\d/\d\d/\d\d, \d?\d:\d\d ' #re for datetime in the chat such as (7/11/19, 8:01 )
    chat_list = re.split(re_date_time, chat_string.lower()) #splitting 
    count = 0
    received = []
    sent = []
    while count < len(chat_list):
        received_msg = ''
        sent_msg = ''
        try:
            while sender_name+':' in chat_list[count]:
                received_msg += chat_list[count].split(':')[2]
                count += 1
            received.append(received_msg)
            while receiver_name+':' in chat_list[count]:
                sent_msg += chat_list[count].split(':')[2]
                count += 1
            sent.append(sent_msg)
        #currently returning value in the except condition as the current logic fails after 
        #reaching end of file. Fix required
        except:
            return (received, sent)