import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from selenium.webdriver.common.keys import Keys

lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
remove_punct_dict['<media omitted>'] = None

def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def response(current_received_message, all_received_messages, sent_messages):
    sent_tokens = all_received_messages #sentence tokens
    robo_response=''
    sent_tokens.append(current_received_message)
    
    TfidVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    sent_tokens.remove(current_received_message)

    if(req_tfidf==0):
        robo_response=robo_response+"Kya mtlb"
        return robo_response
    else:
        robo_response = robo_response+sent_messages[idx]
        return robo_response

def reply_message(sender, all_received_messages, sent_messages, input_box, driver):
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
                    reply = response(user_message, all_received_messages, sent_messages)
                    print("input:"+user_message+"\nOutput:"+reply)
                    input_box.send_keys(reply + Keys.ENTER)
                else:
                    flag=False
                    print('Bye')
            else:
                pass
        except Exception as e:
            print("Exception occured:",e)



