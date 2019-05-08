from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
import operator
from collections import OrderedDict
import pandas as pd
import Tkinter as tkr
from Tkinter import Label 
from Tkinter import Entry
from Tkinter import Button

    
def tokenize_string(question):
    stop = stopwords.words('english')
    newTitle = ''

    list_words = word_tokenize(question.replace("\"",'').lower())
    for i in list_words:
        if i not in stop and i not in string.punctuation:
          newTitle = newTitle + ',' + i

    newTitle = re.sub(r'^,','',newTitle)

    return newTitle

def compare(df, question, tag):
    newTitle = tokenize_string(question.encode('ascii', 'ignore').decode('ascii'))
    qset = set(str(tag).split(',')).union(str(newTitle).split(','))
    jaccard_matrix = {}
    data_dict = {}
    for index, row in df.iterrows():
        id = row['PostId']
        tags = row['Tag1'].encode('ascii', 'ignore').decode('ascii')
        title = row['Title']
        title = title.encode('ascii', 'ignore').decode('ascii')
        data_dict[id] = title

        compareSet = set(str(tags).split(',')).union(str(title).split(','))
        js = jaccard_similarity(qset,compareSet)
        if js > 0.0:
            jaccard_matrix[id] = js

    relevant = {}
    relevant = OrderedDict(sorted(jaccard_matrix.items(), key = operator.itemgetter(1), reverse=True)[:10])
    result = []


    for k, v in relevant.items():
        if k in data_dict:
            
            result.append(data_dict[k])

    return result

def jaccard_similarity(x,y):

    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    return intersection_cardinality/float(union_cardinality)


tk = tkr.Tk()
tk.title("StackOverflow Question Recommender")
frame= tkr.Frame (tk)
frame.pack(fill='both', expand = 0, side = 'top')
mframe = tkr.Frame(tk)
mframe.pack(side = 'top')
bottomframe = tkr.Frame(tk)
bottomframe.pack(side = 'top')
xframe = tkr.Frame(tk)
xframe.pack(side='top')
L1 = Label(frame,text="Enter Your Question: ")
L1.pack(side='left', pady = 20, padx= 5 )
E1 = Entry(frame, width = 75)
E1.insert = 'Input question or search keywords'
E1.pack(side='left', pady = 20, padx = 5)
L2 = Label(mframe, text="Tags [Separated by commas]")
L2.pack(side = 'left', anchor ='w')
E2 = Entry(mframe, width = 10)
E2.pack(side= 'left', anchor = 'w')
LB = tkr.Listbox(xframe, width = 75)
    
def callback():
   
    LB.delete(0,9)
    val = E1.get()
    tag = E2.get()
    df = pd.read_csv('train.csv')
    result = compare(df,val,tag)
    
    i=1
    for row in result:
        LB.insert(i, row)
        ++i
    LB.pack(pady = 10 );


B1 = Button(bottomframe, text='Submit', command = callback)
B2 = Button(bottomframe, text = 'Exit', command = tk.destroy)
B1.pack(side = 'left', ipadx = 10, ipady = 5, padx = 5, pady = 30)
B2.pack(side = 'left', ipadx = 10, ipady = 5, padx = 5, pady = 30)

tk.mainloop()
 
