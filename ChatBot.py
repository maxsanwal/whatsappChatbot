import nltk
import random
import string
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f = open('whatsappChat.txt', encoding="utf8")


raw = f.read()

re_date_time = '\d\d/\d\d/\d\d, \d?\d:\d\d '
chat_list = re.split(re_date_time, raw.lower())

some_chats = chat_list[1:]

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
    

def seperate_received_sent(chat_list, sender, receiver):
    count = 0
    received = []
    sent = []
    while count < len(chat_list):
        received_msg = ''
        sent_msg = ''
        try:
            while sender+':' in chat_list[count]:
                received_msg += chat_list[count].split(':')[2]
                count += 1
            received.append(received_msg)
            while receiver+':' in chat_list[count]:
                sent_msg += chat_list[count].split(':')[2]
                count += 1
            sent.append(sent_msg)
        except:
            return (received, sent)

sender = input("Give Sender Name:").lower()
receiver = input('Give Your name:').lower()


received_messages, sent_messages = seperate_received_sent(some_chats,sender , receiver)

final_length = len(sent_messages) if len(sent_messages) >  len(received_messages) else len(received_messages)

received_messages = received_messages[:final_length]
sent_messages = sent_messages[:final_length]

ent_tokens = received_messages
word_tokens = nltk.word_tokenize(' '.join(word for word in received_messages))

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

remove_punct_dict['<media omitted>'] = None

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def response(received_message):
    robo_response=''
    sent_tokens.append(received_message)
    
    TfidVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_messages[idx]
        return robo_response

driver = webdriver.Chrome('chromedriver/chromedriver')

driver.get("https://web.whatsapp.com")
input("Scan the qr on whatsapp and press enter")

target = input("Enter Sender name same as on your whatsapp")

x_arg = "//span[@title='{}']"

user = driver.find_element_by_xpath(x_arg.format(target))
user.click()

inp_xpath = '//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="6"]'
input_box = driver.find_element_by_xpath(inp_xpath)

def reply_message(sender):
    last_message = ""
    flag = True
    while flag:
        messages_xpath = '//*[contains(@data-pre-plain-text,"{}")]'.format(sender)
        messages = driver.find_elements_by_xpath(messages_xpath)
        user_message = messages[-1].text.lower()
        try:
            if(user_message != last_message):
                last_message = user_message
                if(user_message != 'bye'):
                    reply = response(user_message)
                    print("input:"+user_message+"\nOutput:"+reply)
                    input_box.send_keys(reply + Keys.ENTER)
                    sent_tokens.remove(user_message)
                else:
                    flag=False
                    print('Bye')
            else:
                pass
        except:
            print("Exception occured")

reply_message(target)