import requests
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import pandas as pd 
import tiktoken
import openai
from openai.embeddings_utils import distances_from_embeddings
import numpy as np
from ast import literal_eval
import json
import os
with open('config.json','r') as config_file:
        config_data = json.load(config_file)
        OPENAI_API_KEY = config_data["OPENAI_API_KEY"]  #Setting up the API KEY
openai.api_key = OPENAI_API_KEY
user_direcory = os.getcwd()
file_name = "WS01.txt"  #Text file to store the Scraped data
df_name = "processed_WS01.csv" #csv file to store the preprocessed data
file_path = os.path.join(user_direcory,file_name)
df_path = os.path.join(user_direcory,df_name)
def crawl(url):
    try:
        with open(file_path,"w",encoding="utf-8") as f:
            soup =  BeautifulSoup(requests.get(url).text, "html.parser")
            text = soup.get_text()
            f.write(text)
    except Exception as e:
        print("Error : ",e)
def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie
max_tokens = 500
def split_into_many(text, max_tokens = max_tokens):
    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    chunks = []
    tokens_so_far = 0
    chunk = []
    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue
        chunk.append(sentence)
        tokens_so_far += token + 1
    return chunks

def create_context(question, df, max_len=1800,size="ada"):
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')
    returns = []
    cur_len = 0
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])
    return "\n\n###\n\n".join(returns)
def answer_question(df,question,max_len=1800,size="ada",debug=False,max_tokens=150,stop_sequence=None):
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    if debug:
        print("Context:\n" + context)
        print("\n\n")
    try:
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below.\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=1,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model="text-davinci-003",
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print("Exception : ",e)
        return ""
url = "Provide URL"
crawl(url)
# Preprocessing 
with open(file_path,'r') as f:
    text = f.read()
    data = {'fname':['file'], 'text':[text]}
    df = pd.DataFrame(data)
    df.text = df.fname + ". " + remove_newlines(df.text)
    df.to_csv(df_path)
tokenizer = tiktoken.get_encoding("cl100k_base")
df = pd.read_csv(df_path, index_col=0)
df.columns = ['title','text']
df['n_tokens'] = df.text.apply(lambda x : len(tokenizer.encode(x)))
max_tokens = 500
shortened = []
for row in df.iterrows():
    if row[1]['text'] is None:
        continue
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])
    else:
        shortened.append( row[1]['text'] )
df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
df.to_csv(df_path)
df=pd.read_csv(df_path, index_col=0)
df['embeddings'] = df['embeddings'].apply(literal_eval).apply(np.array)
while(1):
    question = input("Enter a question : ")
    if(question == "Exit"): # Exit condition
        break
    print(answer_question(df,question))
