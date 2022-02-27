
from operator import le
from os import remove
from stop_list import closed_class_stop_words
import math
import re
# import nltk
# nltk.download('punkt')


import sys

queries = []
total_length = 0
queries_TF = {}


# construction of query TFIDS

with open("cran.qry","r") as file: 
    lines = file.readlines()
    init = ""
    for line in lines:
        if(line[0]!="."): init+=line
        else: 
            if(init!=""):
                queries.append(init)
                total_length+=len(init)
                init = ""


for index,value in enumerate(queries):
    query = value.split(' ')
    copy = []
    for word in query:
        if (word not in closed_class_stop_words) & (re.findall('0-9',word) is None): #get rid of numbers
            copy.append(word)
    queries_TF[index] = dict.fromkeys(copy,0)

for index,query in enumerate(queries):
    for word in query.split(" "):
        if word not in closed_class_stop_words:
            for x in range(len(queries)):
                if queries_TF.get(x).get(word) is not None:
                    queries_TF[x][word]+=1
            

for key,value in queries_TF.items():
    for word, fre in value.items():
        queries_TF[key][word] = math.log(total_length / fre)



    

# construction of document TFIDS 

documents = []
abstract_freq = {}


# with open (sys.argv[0],'r') as file:
#     documents_token = nltk.word_tokenize(file)
#     print(documents_token)

with open('cran.all.1400',"r") as file:
    raw_documents = file.readlines()
    init = ""
    for line in raw_documents:
        if line == ".W\n":
            init = ""
        elif line.split()[0] == ".I":
            documents.append(init)
        else:
            init += (line.strip('\n') + " ")

documents = documents[1:] # remove first empty element


documents_filtered = []

for index,abstract in enumerate(documents):
    for word in abstract.split(" "):
        word = word.strip(".,?/!\'\"\\ ")
        if (word not in closed_class_stop_words)& (re.findall(r'[\!\(\)\-\[\]\{\}\;\:\'\"\,\<\>\=\.\/\?\@\#\$\%\^\&\*\_\~]',word)==[])& (re.findall(r'[0-9]',word)==[]):
            documents_filtered.append(word)
    no_duplicate = set(documents_filtered)
    abstract_freq = dict.fromkeys(no_duplicate,0)

def counter_freq_doc(word):
    counter = 0
    for item in documents_filtered:
        if word == item: counter+=1
    return counter

total_document_word = len(documents_filtered)

for word in no_duplicate:
    abstract_freq[word] = round(math.log(total_document_word/counter_freq_doc(word)),5)



# calculation

