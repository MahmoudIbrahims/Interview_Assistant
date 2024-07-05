FILE_PATH =r'Dataset/Ai_pyDev.txt'

import re
import random
import string 
import pickle
import textwrap
import numpy as np
import pandas as pd
import nltk
import warnings
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
warnings.filterwarnings('ignore')
from IPython.display import Markdown
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
import io
import streamlit as st



#============================================================

def open_file_text(file):
  with open(file, 'r', encoding='utf-8') as f:
      data = f.read()
  return data
 #=======================================================
            
def cleaning_text(text): 
    cleantext=re.sub('http\S+',' ', text)
    cleantext = re.sub('RT|cc', ' ',cleantext)
    cleantext=re.sub('#\S+\s',' ',cleantext)
    cleantext = re.sub('@\S+', '  ', cleantext)
    cleantext = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleantext)
    cleantext = re.sub(r'[^\x00-\x7f]', ' ', cleantext) 
    cleantext = re.sub('\s+', ' ', cleantext) 
    
    return cleantext
    
    #=======================================================

        
def Resume(cv):
          
    def cleaning_text(text): 
        cleantext=re.sub('http\S+\s',' ', text)
        cleantext = re.sub('RT|cc', ' ',cleantext)
        cleantext=re.sub('#\S+\s',' ',cleantext)
        cleantext = re.sub('@\S+', '  ', cleantext)
        cleantext = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleantext)
        cleantext = re.sub(r'[^\x00-\x7f]', ' ', cleantext) 
        cleantext = re.sub('\s+', ' ', cleantext) 
    
        return cleantext
    
    with open('model/tfidf.pkl', 'rb') as f:
        tfidf= pickle.load(f)
    
    with open('model/clf.pkl', 'rb') as f:
        clf= pickle.load(f)
                
              # Map category ID to category name
    category_mapping = {
         15: "Java Developer",
         23: "Testing",
         8: "DevOps Engineer",
         20: "Python Developer",
         24: "Web Designing",
         12: "HR",
         13: "Hadoop",
         3: "Blockchain",
         10: "ETL Developer",
         18: "Operations Manager",
         6: "Data Science",
         22: "Sales",
         16: "Mechanical Engineer",
         1: "Arts",
         7: "Database",
         11: "Electrical Engineering",
         14: "Health and fitness",
         19: "PMO",
         4: "Business Analyst",
         9: "DotNet Developer",
         2: "Automation Testing",
         17: "Network Security Engineer",
         21: "SAP Developer",
         5: "Civil Engineer",
         0: "Advocate",
         }
        
    for i in range(len(cv)):
            
        cleaned_resume = cleaning_text(cv)
            # Transform the cleaned resume using the trained TfidfVectorizer
        input_features = tfidf.transform([cleaned_resume])
            # Make the prediction using the loaded classifier
        prediction_id = clf.predict(input_features)[0]
        
        category_name = category_mapping.get(prediction_id, "Unknown")    
        
        return   category_name
        
    #====================================================== 
        
        
def features_extraction(text):
    try:
        Text = text.lower()
        
        phone = re.search(r'\d{6,}', Text)  # Modified phone regex to look for 6 or more digits
        Email_1 = re.search(r'https\S+|hppt\S+', Text)  # Updated email regex
        Email_2 = re.search(r'\S+@\S+', Text)  # Another email regex
        Experience = re.findall(r'experience\s+.+', Text)  # Updated experience regex
        Education = re.findall(r'education\s+.+|graduated\s+.+|graduation\s+.+', Text)  # Updated education regex
        
        data = {'phone': [phone.group() if phone else None],
                'Email_1': [Email_1.group() if Email_1 else None],
                'Email_2': [Email_2.group() if Email_2 else None],
                'Experience': [Experience if Experience else None],
                'Education': [Education if Education else None]}
        
        d_f = pd.DataFrame(data)
        
    except Exception as e:
        print(f'Error: {e}')
        
    return  d_f
    
    #=============================================================
    
def word_tokenizatian(text):
    word_token = nltk.word_tokenize(str(text))
    return word_token
    
    #================================================  
        
        
def sent_tokenizatian(text):
    sent_token = nltk.sent_tokenize(str(text))
    return sent_token
    
#=========================================================
    
def tokenize_stemmer(text):
    stemmer =SnowballStemmer('english')
    tokens=word_tokenizatian(text.lower())
    stemming=[stemmer.stem(w)for w in tokens]
    return " ".join(stemming)

#========================================================

def response(user_input, file_path=FILE_PATH):
    lemmar = nltk.stem.WordNetLemmatizer()

    def toklemma(tokens):
        return [lemmar.lemmatize(tk) for tk in tokens]

    remove_puc_dict = dict((ord(puc), None) for puc in string.punctuation)

    def lemNormalize(text):
        return toklemma(nltk.word_tokenize(text.lower().translate(remove_puc_dict)))

    with open(file_path, 'r',encoding ='utf-8') as file:
        data = file.read()

    def sent_tokenization(text):
        sent_token = nltk.sent_tokenize(str(text))
        return sent_token

    Sent_token =sent_tokenization(data)
    
    # Append user input to the tokenized sentences
    Sent_token.append(user_input)

    tfidfvec = TfidfVectorizer(tokenizer=lemNormalize, stop_words='english')
    tfidf = tfidfvec.fit_transform(Sent_token)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    reg_tfidf = flat[-2]

    if reg_tfidf == 0:
        robo1_res = "I am sorry, I don't understand you"
        return robo1_res
    else:
        robo1_res = Sent_token[idx]
        return robo1_res
    
    
#==================================================================

def similarity(text_1,text_2):
    TFIDF=TfidfVectorizer(tokenizer=tokenize_stemmer,stop_words='english')
    tfidfmatrix =TFIDF.fit_transform([text_1,text_2])
    similar_vector = cosine_similarity(tfidfmatrix)[0][1]
    return similar_vector
    
#=======================================================================
    
    #Create a helper function that will convert the markdown into nicely formatted text
def to_markdown(text):
    text = text.replace('•','*')
    return Markdown(textwrap.indent(text, '>', predicate=lambda _: True))
    
#====================================================================
