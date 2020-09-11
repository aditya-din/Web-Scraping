import pandas as pd
import requests
from bs4 import BeautifulSoup

import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
nlp = spacy.load("en_core_web_sm")

page = requests.get('https://inshorts.com/en/read')
print("-"*100)
print("Web Scraping,Preprocessing and generating Word Cloud of 'inshorts.com' ")
print("*"*70)
print("Status code: ",page.status_code) #status code must be 200
if page.status_code == 200:
    print("*"*70)
    # uncomment just below 2 lines to see page content 
    # print(page.content) # looking at page content
    # print("*"*70)
    soup = BeautifulSoup(page.content,'html.parser')
    print("Page title : ",soup.title.text)
    print("*"*70)
    #finding headlines now
    headline = soup.find_all('span',attrs={'itemprop':"headline"})

    HL=[]  #Head Line
    print("Head Lines of news are : \n")
    for i in headline:
        print(i.text)
        HL.append(i.text)
        print('\n')
    #making it into data frame
    df = pd.DataFrame(HL,columns=['News'])
    print("*"*70)
    print("First five rows of data frame\n",df.head()) #first 5 rows.

    #counting length of tokens in dataframe
    length = []
    for i in range(0,len( df['News'])):
        doc = nlp(df['News'][i])
        length.append(len(doc))
    df['length of token'] = pd.DataFrame(length) 
    # counting number of characters in dataframe
    chars = []
    for i in range(0,len( df['News'])):
        doc = nlp(df['News'][i])
        chars.append(len(doc.text))
    df['Chars'] = pd.DataFrame(chars) 
    # finding punctuation inside data frame
    punc = []
    for i in range(0,len( df['News'])):
        doc = nlp(df['News'][i])
        count=0
        for token in doc:
            if token.is_punct:# is_digit,is_alpha ==> try this also
                count+=1
        punc.append(count)
    df['Punct'] = pd.DataFrame(punc)
    # finding stop words in data frame
    stopWords = []
    for i in range(0,len( df['News'])):
        doc = nlp(df['News'][i])
        count=0
        for token in doc:
            if token.is_stop:#is_digit,is_alpha
                count+=1
        stopWords.append(count)

    df['Stop Word'] = pd.DataFrame(stopWords)
    # calculating number of digits in each row
    digit = []

    for i in range(0,len( df['News'])):
        doc = nlp(df['News'][i])
        count=0
        for token in doc:
            if token.is_digit:#is_digit,is_alpha
                count+=1
        digit.append(count)
    df['Digits'] = pd.DataFrame(digit)
    print("*"*70)

    print("Updated data frame : \n",df.head())
    #Doing preprocessing of text

    # Changing all to lower case beacuse i.e "aditya" = "Aditya"
    def convert_lower(text):
        return text.lower()
   
    for i in range(len(df['News'])):
        df['News'][i] = convert_lower(df['News'][i])
    
    #removing stop word, punctutaion and doing lemmatization
    def process_text(text):
        result=[]
        doc=nlp(text)
        for token in doc:
            if token.text in nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == "-PRON-":
                continue
            result.append(token.text)
        return "".join(result)
    for i in range(len(df)):
        df['News'][i] = process_text(df['News'][i])
    print("*"*70)
    print("Final Data Frame :\n",df.head())
    #print("Full Data Frame :",df)

    # Making Word Cloud of our preprocessed Data Frame
    wc = WordCloud().generate(''.join(df['News']))
    plt.imshow(wc)
    plt.axis('off')
    plt.show
else:
    print("Please Check your internet connectivity\n")
    print("Error Code",page.status_code)
  



            
            
            


            
            
            


    


