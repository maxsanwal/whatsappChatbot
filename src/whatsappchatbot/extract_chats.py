import re

def remove_emoji_newline(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002500-\U00002BEF"  # chinese char
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           u"\n"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

#seperating chats into list of 2 users
def extract_chats(sender_name, receiver_name, chat_file_location):
    #reading the chats into a string
    f = open(chat_file_location, encoding="utf8")
    chat_string = f.read()
    re_date_time = '\d\d/\d\d/\d\d, \d?\d:\d\d ' #re for datetime in the chat such as (7/11/19, 8:01 )
    chat_list = re.split(re_date_time, chat_string.lower())[1:] #splitting 
    count = 0
    received = []
    sent = []
    while count < len(chat_list):
        received_msg = ''
        sent_msg = ''
        try:
            while sender_name.lower()+':' in chat_list[count]:
                received_msg += remove_emoji_newline(chat_list[count].split(':')[1])
                count += 1
            received.append(received_msg)
            while receiver_name.lower()+':' in chat_list[count]:
                sent_msg += remove_emoji_newline(chat_list[count].split(':')[1])
                count += 1
            sent.append(sent_msg)
        #currently returning value in the except condition as the current logic fails after 
        #reaching end of file. Fix required
        except:
            break

    #get the min length to match the sent receive count to 
    # try to keep only the chats which were answered
    final_length = len(sent) if len(sent) <  len(received) else len(received)

    received_messages = received[:final_length]
    sent_messages = sent[:final_length]

    return (received_messages, sent_messages)

    