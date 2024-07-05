from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd

url ='https://www.turing.com/interview-questions/artificial-intelligence'

client =urlopen(url)

html = client.read()

client.close()

soup = bs(html,'html.parser') 

containers =soup.find_all("div",{"class":"OrderedBlocks_section__SLmhw"})

len(containers)

bs.prettify(containers[0])

f= open ('Dataset/AI_for_interview.txt','w',encoding ='utf-8')
#header ='Questian_Ai, Answering_Ai,'
#f.write(header)

for container in containers:
    Questian_Ai =container.findAll("div",{"class": "RichText_root__TVuc9 OrderedBlocks_question__DKDfv"})
    Questian_Ai =Questian_Ai[0].text.strip()
    
    Answering_Ai = container.findAll('div',{"class" :"RichText_root__TVuc9 OrderedBlocks_answerText__rgqDt"})
    Answering_Ai =Answering_Ai[0].text.strip()
    
    f.write( Questian_Ai + ',' + Answering_Ai +'\n')
f.close()
    
