import pandas as pd
import numpy as np 
import plotly
import plotly.express as px
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
import pickle

FILE_PATH='Dataset/Data_for_Resume.csv'

template_style = "plotly_white"

df=pd.read_csv(FILE_PATH)
df.head()

df.isnull().sum()

df.info()

f =open('Dataset/cv_python_Dev','w',encoding ='utf-8')
python_Dev =df[df['Category']=='Python Developer']['Resume'][551]
f.write(python_Dev)
f.close()

df['Resume'].sample(1).iloc[0]

def cleaning_text(text): 
    cleantext=re.sub('http\S+\s',' ', text)
    cleantext = re.sub('RT|cc', ' ',cleantext)
    cleantext=re.sub('#\S+\s',' ',cleantext)
    cleantext = re.sub('@\S+', '  ', cleantext)
    cleantext = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleantext)
    cleantext = re.sub(r'[^\x00-\x7f]', ' ', cleantext) 
    cleantext = re.sub('\s+', ' ', cleantext) 
    
    return cleantext



df['Resume']=df['Resume'].apply(lambda x:cleaning_text(x))

df['Resume'].sample(1).iloc[0]

df_categort=df['Category'].value_counts().reset_index().sort_values('Category',ascending=False)


### Visualization

# Create Chart
fig = px.bar(df_categort,
              x='index',
              y='Category',
              template = template_style,
              title= '<b>Number of jobs</b>')

# Display Plot
fig.show()

#### Get a view of unique values in column, e.g. 'Category'

df['Category'].unique()


### convert categort to Numbers
le = LabelEncoder()
le.fit(df['Category'])
df['Category'] = le.transform(df['Category'])



df['Category'].unique()


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

### convert Resume text to TFIDF

tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit(df['Resume'])
requredText  = tfidf.transform(df['Resume'])


## spliting Data
X_train, X_test, y_train, y_test = train_test_split(requredText, df['Category'], test_size=0.2, random_state=42)

### Create Model for Prediction

clf = OneVsRestClassifier(KNeighborsClassifier())
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)


### show results predict
d_f=[]
for i in y_pred:
    d_f.append(category_mapping.get(i, "Unknown"))
    
d_f[:10]


#accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
print(classification_report(y_test,y_pred))


## save model and TFIDF
pickle.dump(tfidf,open('tfidf.pkl','wb'))
pickle.dump(clf, open('clf.pkl', 'wb'))


#### open file resume
with open('Dataset/mahmoudibrahim.TXT','r')as f:
    data=f.read()
data  


### test the model
def Resume(cv):
    for i in range(len(cv)):
        cleaned_resume = cleaning_text(cv)
        # Transform the cleaned resume using the trained TfidfVectorizer
        input_features = tfidf.transform([cleaned_resume])
        # Make the prediction using the loaded classifier
        prediction_id = clf.predict(input_features)[0]
        
        category_name = category_mapping.get(prediction_id, "Unknown")    
        
        return   category_name
              
        
Resume(data)

