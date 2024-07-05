from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd

url ="https://www.turing.com/interview-questions/python"

client =urlopen(url)

html = client.read()

client.close()

soup = bs(html,'html.parser') 

containers =soup.find_all("div",{"class":"OrderedBlocks_section__SLmhw"})

len(containers)

bs.prettify(containers[0])

f= open ('Dataset/python_developer_interview.txt','w',encoding ='utf-8')
#header ='Questian_py, Answering_py,'
#f.write(header)
     

for container in containers:
    Questian_py =container.findAll("div",{"class": "RichText_root__TVuc9 OrderedBlocks_question__DKDfv"})
    Questian_py =Questian_py[0].text.strip()
    
    Answering_py = container.findAll('div',{"class" :"RichText_root__TVuc9 OrderedBlocks_answerText__rgqDt"})
    Answering_py =Answering_py[0].text.strip()
    
    f.write( Questian_py + ',' + Answering_py +'\n')
f.close()


files=["Dataset/AI_for_interview.txt","Dataset/python_developer_interview.txt"]
with open("Ai_pyDev.txt","w",encoding='utf-8')as f: 
    for file in files:
        with open(file,"r",encoding='utf-8')as fr:  
            for line in fr:
                f.write(line)
