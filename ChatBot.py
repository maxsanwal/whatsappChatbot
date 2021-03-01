#!/usr/bin/env python
# coding: utf-8

# In[182]:


import nltk
import numpy as np
import random
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[204]:


f = open('whatsappChat.txt', encoding="utf8")


# In[205]:


raw = f.read()


# In[206]:


chat_list = raw.lower().split('\n')


# In[208]:


training_chat_count = int(input("Enter number of chats you want to train with"))


# In[209]:


some_chats = chat_list[:training_chat_count]


# In[210]:


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


# In[211]:


sender = input("Give Sender Name:").lower()
receiver = input('Give Your name:').lower()


# In[ ]:


received_messages, sent_messages = seperate_received_sent(some_chats,sender , receiver)


# In[82]:


final_length = len(sent_messages) if len(sent_messages) >  len(received_messages) else len(received_messages)


# In[83]:


received_messages = received_messages[:final_length]
sent_messages = sent_messages[:final_length]


# In[84]:


sent_tokens = received_messages
word_tokens = nltk.word_tokenize(' '.join(word for word in received_messages))


# In[85]:


lemmer = nltk.stem.WordNetLemmatizer()


# In[86]:


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


# In[87]:


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


# In[88]:


remove_punct_dict['<media omitted>'] = None


# In[89]:


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# In[90]:


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


# In[174]:


driver = webdriver.Chrome('chromedriver/chromedriver')


# In[175]:


driver.get("https://web.whatsapp.com")
input("Scan the qr on whatsapp and press enter")


# In[176]:


target = input("Enter Sender name same as on your whatsapp")


# In[177]:


x_arg = "//span[@title='{}']"


# In[178]:


user = driver.find_element_by_xpath(x_arg.format(target))
user.click()


# In[179]:


inp_xpath = '//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="6"]'
input_box = driver.find_element_by_xpath(inp_xpath)


# In[180]:


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


# In[181]:


reply_message(target)


# In[ ]:




