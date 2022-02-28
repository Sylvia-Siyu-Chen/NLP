
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
queries_IDF = {}
queries_TFIDF = {}
query_filtered_words = []



# construction of query TFIDS

with open("cran.qry","r") as file: 
    lines = file.readlines()
    init = ""
    for line in lines:
        if(line[0]!="."): init+=line.strip('\n\r')+" "
        else: 
            if(init!=""):
                queries.append(init)
                total_length+=len(init)
                init = ""


for index,value in enumerate(queries):
    query_filtered = []
    query = value.split(' ')
    for word in query:
        if (word not in closed_class_stop_words)& (re.findall(r'[\!\(\)\-\[\]\{\}\;\:\'\"\,\<\>\=\.\/\?\@\#\$\%\^\&\*\_\~]',word)==[])& (re.findall(r'[0-9]',word)==[]):
            query_filtered.append(word)
    queries_TF[index] = dict.fromkeys(set(query_filtered),0)
    queries_TFIDF[index] = dict.fromkeys(set(query_filtered),0)
    query_filtered_words.append(query_filtered)


total_queries = len(queries)
    

for index,query in enumerate(queries):
    for word in query.split(" "):
        word = word.strip("\n\r ,./?")
        if word in queries_TF.get(index).keys():
            queries_TF[index][word] += 1
            

def IDF_query(word):
    counter = 0
    for list in query_filtered_words:
        if word in list: counter +=1
    return counter

for key, value in queries_TF.items():
    for word, times in value.items():
        queries_IDF[word] = math.log(total_queries/IDF_query(word))
        queries_TFIDF[key][word] = times * math.log(total_queries/IDF_query(word))

# for k,v in queries_TFIDF.items():
#     print(k,v)

# construction of document TFIDS 

documents = []
abstract_TF = {}
abstract_IDF = {}
abstract_TFIDF = {}
abstract_filtered_words = []



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



for index,abstract in enumerate(documents):
    documents_filtered = []
    for word in abstract.split(" "):
        word = word.strip(".,?/!\'\"\\ ")
        if (word not in closed_class_stop_words)& (re.findall(r'[\!\(\)\-\[\]\{\}\;\:\'\"\,\<\>\=\.\/\?\@\#\$\%\^\&\*\_\~]',word)==[])& (re.findall(r'[0-9]',word)==[]):
            documents_filtered.append(word)
    no_duplicate = set(documents_filtered)
    abstract_TF[index] = dict.fromkeys(no_duplicate,0)
    abstract_TFIDF[index] = dict.fromkeys(no_duplicate,0)
    abstract_filtered_words.append(documents_filtered)



for index, abstract in enumerate(documents):
    for word in abstract.split(" "):
        word = word.strip("\n\r ,./?")
        if word in abstract_TF.get(index).keys():
            abstract_TF[index][word]+=1

def IDF_abstract(word):
    counter = 0
    for list in abstract_filtered_words:
        if word in list: counter +=1
    return counter


total_abstracts = len(documents)
# print(total_abstracts)

for key, value in abstract_TF.items():
    for word, times in value.items():
        abstract_IDF[word] = math.log(total_abstracts/IDF_abstract(word))
        abstract_TFIDF[key][word] = times * math.log(total_abstracts/IDF_abstract(word))

# for k,v in abstract_TFIDF.items():
#     print(k,v)


# calculate cosine similarities 


def cosine_similarity(query,document):
    numerator = 0
    denominator_q = 0
    denominator_d = 0
    # print(query,document)
    for index,score in enumerate(query):
        # print(index,score)
        if score != 0:
            numerator += score*document[index]
            denominator_q += math.pow(score,2)
        denominator_d += math.pow(document[index],2)
    # print(numerator, math.sqrt(denominator_d*denominator_q))
    if(math.sqrt(denominator_d*denominator_q)!= 0): return (numerator / math.sqrt(denominator_d*denominator_q))
    else: return 0



def calculate_vectors(query,index):
    abstract_rank = {}
    for key, value in abstract_TFIDF.items():
        q_vector = []
        a_vector = []
        for q in query:
            if q in value.keys():
                q_vector.append(queries_TFIDF[index][q])
                a_vector.append(value.get(q))
        cosine = cosine_similarity(q_vector,a_vector)
        abstract_rank[key] = cosine
    return abstract_rank


output = {}

for index, query in queries_TFIDF.items():
    output[index] = calculate_vectors(query, index)


with open("output.txt","w") as file:
    for k,v in output.items():
        for key, value in sorted(v.items(), key=lambda x:x[1],reverse=True):
            file.write(str(k+1) + " " + str(key) + " " + str(value))
            file.write('\n')
    file.close()


    






