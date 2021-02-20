#!/usr/bin/env python
# coding: utf-8

# In[59]:


import nltk
import numpy as np
import random
import string


# In[60]:


f = open('whatsappChat.txt')


# In[61]:


raw = f.read()


# In[62]:


chat_list = raw.lower().split('\n')


# In[88]:


training_chat_count = 4001


# In[89]:


some_chats = chat_list[:training_chat_count]


# In[90]:


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


# In[91]:


sender = input("Give Sender Name")
receiver = input('Give Your name')


# In[92]:


received_messages, sent_messages = seperate_received_sent(some_chats,sender , receiver)


# In[93]:


# import pickle

# with open('sender.pkl', 'wb') as f:
#   pickle.dump(received_messages, f)
# with open('receiver.pkl', 'wb') as f:
#   pickle.dump(sent_messages, f)


# In[94]:


final_length = len(sent_messages) if len(sent_messages) >  len(received_messages) else len(received_messages)


# In[95]:


received_messages = received_messages[:final_length]
sent_messages = sent_messages[:final_length]


# In[96]:


sent_tokens = received_messages
word_tokens = nltk.word_tokenize(' '.join(word for word in received_messages))


# In[99]:


lemmer = nltk.stem.WordNetLemmatizer()


# In[100]:


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


# In[101]:


remove_punct_dict['<media omitted>'] = None


# In[102]:


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# In[103]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[104]:


from sklearn.metrics.pairwise import cosine_similarity


# In[105]:


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


# In[ ]:


flag=True
while(flag==True):
    user_message = input()
    user_message = user_message.lower()
    if(user_message != 'bye'):
        print(response(user_message))
        sent_tokens.remove(user_message)
    else:
        flag=False
        print('Bye')


# In[ ]:




