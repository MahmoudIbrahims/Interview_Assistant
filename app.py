import re
import pickle
import pandas as pd
import numpy as np
from datetime import date
from io import BytesIO
from PyPDF2 import PdfReader
from langchain_community.document_loaders import Docx2txtLoader
import streamlit as st
import random
import time
from docx import Document
# Preprocessing functions (assuming they are already defined)
from preprocessing import (
    open_file_text, cleaning_text, Resume,
    features_extraction, word_tokenizatian, sent_tokenizatian, 
    tokenize_stemmer, response, similarity, to_markdown
)

FILE_PATH = r'Dataset/Ai_pyDev.txt'
data = open_file_text(FILE_PATH)
sent_token = sent_tokenizatian(data)
word_token = word_tokenizatian(data)

greet_input = ['hey', 'helo', 'greetings', 'sup', 'whats up', 'hi']
greet_response = ['hey dear', 'helo dear', 'hi there', 'whats going one', 'I am glad! you are talking to me']

Score = []
Data = []
Date = []

def Extract_information(DATA):
    columns = ['phone', 'Email_1', 'Email_2', 'Experience', 'Education']
    df = pd.DataFrame(columns=columns)
    data = pd.concat([DATA, df], axis=0)
    Data.append(data)

sent_token = sent_tokenizatian(data)

def ChatBot(data):
    st.write('''Assistant HR: hey my name is ZOOX, I am an artificial intelligence program to help you get the job. 
           Let's have a conversation. If you want to exit just write Bye!''')
    st.write()

    today = date.today()
    st.write('Interview date is:', today)
    Date.append(today)
    st.write()

    Features = features_extraction(data)
    Extract_information(Features)

    predict = Resume(data)
    st.write('Job Expected =', predict)

    if predict == 'Data Science':
        questions = [
            'How are machine learning and AI related?',
            'We use AI to build various applications for example?',
            'Explain Artificial Intelligence and give its applications?',
            'Give some examples of weak and strong AI?'
        ]

        total_similarity = 0
        for i, question in enumerate(questions):
            user_answer = st.text_input(question, key=f"question_{i}")
            if user_answer:
                user_answer = user_answer.lower()
                similarity_score = similarity(user_answer, response(question))
                st.write(f"The Similarity of your Answer and correct answer is = {similarity_score}")
                total_similarity += similarity_score
                

        total = (total_similarity / len(questions)) * 100
        st.write("The Score of The interview =", total)
        Score.append(total)

    elif predict == 'Python Developer':
        question = 'What built-in types are available in Python?'
        user_answer = st.text_input(question)
        if user_answer:
            user_answer = user_answer.lower()
            similarity_score = similarity(user_answer, response(question))
            st.write(f"The Similarity of your Answer and correct answer is = {similarity_score}")
            Score.append(similarity_score)

    

def show_data():
    return Score, Date, Data

def details_interview(Score, Date, Data):
    score = np.array(Score)
    score = pd.Series(score, name='Score')
    score = pd.DataFrame(score)
    score['interview date'] = pd.to_datetime(Date)
    columns = ['phone', 'Email_1', 'Email_2', 'Experience', 'Education']
    data = np.reshape(Data, (-1, 5))
    data = pd.DataFrame(data, columns=columns)
    DATA = pd.concat([score, data], ignore_index=False, axis=1)
    return DATA

st.set_page_config(
    page_title="Interview Testing",
    page_icon="🔥"
)

st.title("Chat with Interview Testing")
st.caption("It was made by team Amani")

def get_pdf_text(pdf):
    pdf_reader = PdfReader(BytesIO(pdf))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def get_docx_text(docx_bytes):
    document = Document(BytesIO(docx_bytes))
    doc_text = ""
    for para in document.paragraphs:
        doc_text += para.text + "\n"
    return doc_text

def main():
    st.header("Interview Testing")
    with st.sidebar:
        st.title("Settings")
        st.subheader("Upload your CV")
        Resume = st.file_uploader("Please upload the CV", type=["pdf", "docx"], accept_multiple_files=False)
        
        if "raw_texts" not in st.session_state:
            st.session_state.raw_texts = []
        
        if st.button("Process"):
            with st.spinner("Processing"):
                if Resume is not None:
                    if Resume.name.endswith(".pdf"):
                        raw_text = get_pdf_text(Resume.read())
                        st.session_state.raw_texts.append(raw_text)
                    elif Resume.name.endswith(".docx"):
                        raw_text = get_docx_text(Resume.read())
                        st.session_state.raw_texts.append(raw_text)
                    st.success("Done")
                else:
                    st.error("Please upload a file")
                    
    if st.session_state.raw_texts:
        st.session_state.conversation = ChatBot(st.session_state.raw_texts[-1])
        Score, Date, Data = show_data()
        data = details_interview(Score, Date, Data)
        data.to_excel('result_HR.xlsx')
         
    user_response = st.text_input('Ask a Question')
    if user_response:
          if "chatHistory" not in st.session_state:
              st.session_state.chatHistory = []
          if user_response in greet_input:
              st.session_state.chatHistory.append(('Assistant HR', random.choice(greet_response)))
          elif user_response.lower() != 'bye':
              if user_response.lower() in ["thanks", "thank you"]:
                  st.session_state.chatHistory.append(("Assistant HR", "You are Welcome"))
              else:
                  sent_token.append(user_response)
                  word_tokens = word_token + word_tokenizatian(user_response)
                  final_words = list(set(word_tokens))
                  st.session_state.chatHistory.append(("Assistant HR", response(user_response)))
                  sent_token.remove(user_response)
          else:
              st.session_state.chatHistory.append(('Assistant HR', 'Ok, Goodbye! Take Care'))

          for speaker, message in st.session_state.chatHistory:
              st.write(f"{speaker}: {message}")

          if st.button("Clear Chat History"):
              st.session_state.chatHistory = []

if __name__ == "__main__":
    main()
