from preprocessing import open_the_file,cleaning_text,Resume,get_CV_pdf
from preprocessing import features_extraction,word_tokenizatian,sent_tokenizatian
from preprocessing import tokenize_stemmer,response,similarity,to_markdown
from datetime import date
import pandas as pd
import numpy as np 

FILE_PATH =r'Dataset/Ai_pyDev.txt' 

data= open_the_file(FILE_PATH)

sent_token=sent_tokenizatian(data)

word_token =word_tokenizatian(data)

greet_input = ['hey','helo','greetings','sup','whats up','hi']

greet_response = ['hey dear','helo dear ','hi there','whats going one','I am glad! you are talking to me']


Score =[]
Data =[]
Date=[]

def Extract_informatian(DATA):
    
    columns =['phone','Email_1','Email_2','Experience','Education']    
    df =pd.DataFrame(columns =columns)
    data =pd.concat([DATA,df],axis =0)
    Data.append(data)
    

sent_token=sent_tokenizatian(data)    

def ChatBot(data):
    
    flag =True
    
    print('''Bot: hey me name is Gamie,i am an artificial intelligence program to help you get the job, 
           Let's have a conversation. If you want to exit just write Buy!''')
    print()
    #display(Image(filename =image_path, width =200, height =400))
    
    while flag==True:
        
        #input_user =input('please write to path the Resume :')
        
        #data =open_the_file(input_user)
        #data =get_CV_pdf(input_user)
        
        
        print()
        #print()
        today =date.today()
        print('interview date is :',today)
        Date.append(today)
        #print()  
        print()
        
        Features =features_extraction(data)
        #print(Features)
        Extract_informatian(Features)
        
        predict =Resume(data)
        print()
        print( 'job Expected  =' , predict)
        
        if predict =='Data Science':
            
            
            questian1 =str(input('How are machine learning and AI related?'))
            questian1 =questian1.lower()
            similarity1 =similarity(questian1,response('How are machine learning and AI related?'))
            print("The Similarity of your Answer and correct answer dear = ",similarity1)
    
            questian2 =str(input('We use AI to build various applications for example ?'))
            questian2 = questian2.lower()
            similarity2 =similarity(questian2,response('We use AI to build various applications for example ?'))
    
            print("The Similarity of your Answer and correct answer dear = ",    similarity2)
    
            questian3 =str(input('Explain Artificial Intelligence and give its applications?'))
            questian3 =questian3.lower()
            similarity3 =similarity(questian3,response('Explain Artificial Intelligence and give its applications?'))
    
            print("The Similarity of your Answer and correct answer dear = ",similarity3)

            questian4 =str(input('Give some examples of weak and strong AI?'))
            questian4 = questian4.lower()
            similarity4 = similarity(questian4,response('Give some examples of weak and strong AI?'))
            print("The Similarity of your Answer and correct answer dear  = ", similarity4)
            print('----------')
            total =(similarity1+similarity2+similarity3+similarity4)/4*100 
            print("The Score of The interview =",total)
            Score.append(total)
            flag =False
        
           
        elif predict =='Python Developer':
           
            questian1 =str(input('What built-in types are available in Python?'))
            questian1 =questian1.lower()
            similarity1 =similarity(questian1,response('What built-in types are available in Python?'))
            print("The Similarity of your Answer and correct answer dear = ",similarity1)
            Score.append(similarity1)
            flag =False
            break
            
    for i in range(0,1000):
        user_response=input('you')   
        if user_response in greet_input:
            print('Bot :',random.choice(greet_response))
    
        elif user_response !='buy':
            if user_response=="thanks" or user_response=='thank you':
                flag=False
                print("Bot: You are Welcome")
                break
            else:
                sent_token.append(user_response)
                word_tokens =word_token+word_tokenizatian(user_response)
                final_words = list(set(word_tokens))
            
                print("Bot:",end="")
                print('-'*5)
                print(response(user_response))
                sent_token.remove(user_response)     
            
        else:
        
            flag=False
            print('Bot: Ok Good Buy! Take Care')
            break
            
            

def show_data():
    return Score,Date,Data
            
def details_interview(Score,Date,Data):
    """
    the functian to make combination All Data
    
    """
    score =np.array(Score)
    score=pd.Series(score,name='Score')
    score =pd.DataFrame(score)
    score['interview date'] =pd.to_datetime(Date)
    columns =['phone','Email_1','Email_2','Experience','Education']
    data=np.reshape(Data,(-1,5))
    data =pd.DataFrame(data,columns=columns)
    DATA=pd.concat([score,data],ignore_index =False,axis=1) 
    return DATA


