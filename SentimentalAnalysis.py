#!/usr/bin/env python
# coding: utf-8

# INSTRUCTIONS:
# 
# Required Dependensies:
# Installation of : nltk, pandas,bs4,request
# 
# Downloads from nltk:
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('cmudict')
# 
# Folders provided vai google drive
# 
# Python IDE
# 
# Run the below code with folder path of each folder to get the output in the Excel(xlsx) format. 

# In[32]:


#import require libraries
import nltk 
import pandas as pd
from nltk.corpus import stopwords
import re
import os
from nltk.corpus import stopwords
from nltk.corpus import cmudict
import requests
from bs4 import BeautifulSoup as bs

CMU_DICT = cmudict.dict()

def getContent(url): #gets title and content of the web page
    page = requests.get(url)
    if page.status_code == 200:
        soup = bs(page.text,'html')
        title_tags = soup.find('title')
        divs_tags = soup.find('div', class_ = 'td-post-content')
        if title_tags and divs_tags:  
            title = title_tags.get_text()
            divs = [div.get_text() for div in divs_tags]
            content = ' '.join(divs + [title])
            return content
        else:
            print("Title or content not found for URL:", url)
    else:
        print("Failed to fetch URL:", url) #if status code is not 200 return None
    return None 


def readStopwords(folder_path):
    stopwords = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path,filename)
        with open(file_path, 'r') as file:
            word = file.readlines()
            stopwords.append(word) #get stop words from file
    return stopwords

def MasterDict():
    folder_path = "folder//path.."
    master_dict = {'positive': [], 'negative': []}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            word = [word.strip() for word in file.readlines()]
            if 'positive' in filename.lower():
                master_dict['positive'].extend(word)
            elif 'negative' in filename.lower():
                master_dict['negative'].extend(word) #get positive and negative words from file
            else:
                pass
    return master_dict

def read_urls():
    url_path = "folder//path.."
    df = pd.read_csv(url_path)
    urls = df['URL'].tolist()
    return urls #get only urls from input file

def count_syllables(word, CMU_DICT): # use to check for the syllables
    syllables = CMU_DICT.get(word.lower())
    if syllables:
        return [len(list(y for y in x if y[-1].isdigit())) for x in syllables][0]
    else:
        return 0

def count_complex_words(text): #used to count the complex words and number of syllables in it
    complex_count = 0
    c_syllables = 0
    words = nltk.word_tokenize(text)
    for word in words:
        syllables = count_syllables(word, CMU_DICT)
        c_syllables += syllables
        if syllables > 2:
            complex_count += 1
    return complex_count, c_syllables 
    
def count_words(text): #get number of words
    words = nltk.word_tokenize(text)
    words = [re.sub(r'[^\w\s]', '', word) for word in words]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    return len(words)
    
    return words

def count_personal_pronouns(text): #get number of personal prnouns
    pattern = r'\b(?:I|we|my|ours|us)\b'
    regex = re.compile(pattern, flags=re.IGNORECASE)
    matches = regex.findall(text)
    return len(matches)

def TextAnalysis(): #also main funtion
    results = []
    fox_index = 0
    average_number_of_words_per_sentence = 0
    complex_count = 0
    word_count = 0
    syllable_count_per_word = 0
    personal_pronounce = 0
    average_word_lenght = 0
    stop_words_path = "folder//path.."
    urls = read_urls()
    master_dict = MasterDict()
    stopwords = readStopwords(stop_words_path)
    lm = WordNetLemmatizer()
    for url in urls:
        positive_score = 0
        negative_score = 0
        ASL = 0
        complex_per = 0
        fox_index = 0
        average_words_per_sent = 0
        n_syllables = 0
        Word_count = 0
        n_personal = 0
        AWL = 0
        C_words = []
        content = getContent(url)
        if content is not None:
            cleaned_content = re.sub(r'[^a-zA-Z\s.]', '', content)
            
            words = nltk.word_tokenize(cleaned_content)
            AWL = sum(len(word) for word in words) / len(words)
            for word in words:
                if word not in stopwords:     
                    if word.lower() in master_dict['positive']:
                        positive_score += 1
                    elif word.lower() in master_dict['negative']:
                        negative_score +=1
                    else:
                        pass
                    C_words.append(word)
                    len_C_words = len(C_words)
                    
            subjective_score = (positive_score + negative_score)/((len_C_words) + 0.000001)
            polarity_score = (positive_score - negative_score)/((positive_score + negative_score) + 0.000001)
            C_content = " ".join(C_words)
            
            n_words = len(nltk.word_tokenize(cleaned_content))
            n_sen = len(nltk.sent_tokenize(cleaned_content))
            ASL = n_words/n_sen
            n_complex,n_syllables = count_complex_words(content)
            complex_per = n_complex/n_words
            fox_index = 0.4 * (ASL + complex_per)
    
            Word_count = count_words(cleaned_content)
            n_personal = count_personal_pronouns(cleaned_content)
    
            average_words_per_sent = ASL
            results.append([url, positive_score, negative_score, subjective_score, polarity_score, ASL, complex_per, fox_index, ASL, n_complex, Word_count, n_syllables, n_personal, average_words_per_sent])
            print(results)
    df = pd.DataFrame(results, columns=['URL', 'Positive Score', 'Negative Score', 'Subjective Score', 'Polarity Score', 'Average Sentence Length', 'Complex Word Percentage', 'Fog_Index', 'Average Number of Words Per Sentence', 'Complex word count', 'Word_Count', 'Syllable count','Personal_Pronouns_Count', 'Average_Words_Per_Sentence'])
    df.to_excel("folder//path//to//save..", index=False)


# In[33]:


TextAnalysis() #run main funtions 


# In[ ]:




