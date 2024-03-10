import tensorflow as tf
import numpy as np
import pandas as pd
import sqlite3
import google.generativeai as gen
import nltk
from nltk.metrics import edit_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import requests
import pickle
from dotenv import load_dotenv
import os
load_dotenv('API.env')


class GENAI():
    
    def __init__(self):
        load_dotenv()
        data = pd.read_csv('Batting_lower.csv',index_col=0)
        data['date_of_birth']=pd.to_datetime(data['date_of_birth'])
        data['date_of_death']=pd.to_datetime(data['date_of_death'])
        data['matchdate']=pd.to_datetime(data['matchdate'])
        data.drop(['matchid'],axis=1,inplace=True)

        self.players_data = data['player_name'].unique()
        self.stop = nltk.corpus.stopwords.words('english')

        self.tf = pickle.load(open("tf.pickle", "rb"))
        col = ','.join(list(data.columns))

        with open('prompt.text','r') as m:
            prompt = m.readlines()
            self.prompt = ' '.join(prompt)     
        with open('prompt_output.text','r') as m:
            prompt_out = m.readlines()
            self.prompt_out = ' '.join(prompt_out)     
        
        self.db = sqlite3.connect('ODI.db')
        data.to_sql('ODI',self.db,if_exists='replace')

        gen.configure(api_key= os.getenv('API_KEY'))
        config = {'temperature':0.4, 'top_p':1, 'top_k':32}
        self.model = gen.GenerativeModel('gemini-pro', generation_config=config)
        
    def extract_name(self, user):
        y = self.tf.transform([user])
        similarities = cosine_similarity(self.tf.transform(self.players_data), y)
        names_6 = []
        names_45 = []
        for i,s in enumerate(similarities):
            if(s>0.6):
                if(i not in names_6):
                    names_6+=[self.players_data[i]]
            elif(s>0.40):                         # checking with 0.40 prob score
                if(i not in names_45):
                    names_45+=[self.players_data[i]]
        return names_45 if len(names_6)==0 else names_6

    def preprocess(self, text='How many runs did virat ,ishant, rohit scored in 2019'):
        text = text.strip().lower()
        text = re.sub(r"[^a-zA-Z0-9.\s]+", '', text)
        text = nltk.tokenize.word_tokenize(text)
        final_text = []
        for i in text:
            if i not in self.stop:
                final_text+=[i]
        return final_text

    def rephrase(self, text, comparison=0):
        text = text.lower()
        rephrases = []
        preprocessed = self.preprocess(text)
        if comparison==0:
            for i in preprocessed:
                one = self.extract_name(i)
                if len(one)!=0:
                    if len(one)==1:
                        text = re.sub(i, one[0], text)
                    else:
                        for j in one:
                            rephrases+=[re.sub(i, j, text)]
            return [text] if len(rephrases)==0 else rephrases
        else:
            final = []
            for i in preprocessed:
                one = self.extract_name(i)
                if len(one)!=0:
                    final+=[one]
            return final
                                
    def query_sql(self, code, db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(code)
        rows = cur.fetchall()
        conn.close()
        return rows

    def genai(self, prompt, question):
        output = self.model.generate_content([prompt, question])
        return output

    def output(self, question):
        question = self.rephrase(question.lower())
        out = []
        for i in question:
            out+=[self.genai(self.prompt, i).text]
        with open("test.sql", "w") as f:
            for i in out:
                f.write(re.sub('```', '', re.sub('```sql', '', i)))
        with open('test.sql', 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
        answer_text = []
        for i in range(len(question)):
            answer_text+=[self.genai(self.prompt_out, question[i]+'~'.join(map(str, self.query_sql(sql_commands[i], 'ODI.db')[0]))).text]
        return answer_text


# print(os.getenv('API_KEY'))
# GENai = GENAI()
# print(GENai.output('How many times did Finch got out by Bhuvaneshwar?'))
