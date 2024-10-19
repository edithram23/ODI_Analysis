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
from pymongo import MongoClient
import base64
from io import BytesIO
from PIL import Image
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('punkt')

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
        
    def extract_name(self, user,sim=0.6):
        y = self.tf.transform([user])
        similarities = cosine_similarity(self.tf.transform(self.players_data), y)
        names_6 = []
        names_45 = []
        print(len(self.players_data))
        for i,s in enumerate(similarities):
            if(s>sim):
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
        question = self.rephrase(question.lower()+'?')
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

    
    
    
    def ind_output(self,name):
        questions = [f'How many matches has {name} played?',f'How many runs has {name} scored?',f'What is run average of {name}?',f'How many fifties has {name} scored?',
                     f'How many centuries have {name} scored?',f'How many fours have {name} hit?',f"How many sixes have {name} scored"]
        out = []
        for i in questions:
            out+=[self.genai(self.prompt, i).text]
            # print(out)
        with open("test.sql", "w") as f:
            for i in out:
                f.write(re.sub('```', '', re.sub('```sql', '', i)))
        with open('test.sql', 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
        answer_text = []
        for i in range(len(questions)):
            answer_text+=[''.join(map(str,self.query_sql(sql_commands[i], 'ODI.db')[0]))]
            num = float(answer_text[i])
        
            # If the number is effectively an integer (e.g., 36.00), convert it to int
            if num.is_integer():
                answer_text[i] = str(int(num))
            else:
                # Otherwise, format to 2 decimal places
                answer_text[i] = "{:.2f}".format(num)
        return answer_text

class Comparison():
    def __init__(self):
        self.uri = os.getenv('mongodb')
        self.client = MongoClient(self.uri)
        self.db = self.client['ODI']
        self.collection = self.db.player_image
    def trim_transparency(self,img):
        if img.mode == 'RGBA':
            # Get bounding box of non-transparent pixels
            bbox = img.getbbox()
            if bbox:
                img = img.crop(bbox)
        return img

    def image_retrieve(self,name,file='image'):
        documents = list(self.collection.find({ 'Player_name': name }))[0]
        # decoded_data = base64.b64decode(documents['Orginal'])
        # image_buffer = BytesIO(decoded_data)
        # image = Image.open(image_buffer)
        # image.save(file+'.jpg')
        decoded_data = base64.b64decode(documents['Removed'])
        image_buffer = BytesIO(decoded_data)
        image = Image.open(image_buffer)
        trimmed_image = self.trim_transparency(image)
        print("123")
        
        # trimmed_image.save('../frontend/odifront/src/assets/images/'+file+'.png')
        output_buffer = BytesIO()
        trimmed_image.save(output_buffer, format="PNG")
        base64_encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        # Return Base64 encoded image
        return base64_encoded_image
    def output(self,name1,name2):
        try:
            image1 = self.image_retrieve(name1,file='image1')
        except:
            image1 = self.image_retrieve(name='Kedar Jadhav',file='image1')
            print('Key error',name1)
        try:
            image2= self.image_retrieve(name2,file='image2')
        except:
            image2=self.image_retrieve(name='Kedar Jadhav',file='image2')
            print('Key error',name2)
        return image1,image2
# Com = Comparison()
# Com.image_retrieve('Virat Kohli')

# print(os.getenv('API_KEY'))
# GENai = GENAI()
# print(GENai.output('How many times did Finch got out by Bhuvaneshwar?'))


"""
        - Output
            - Rephrase = rephrases for different player names
                - Preprocess = stopword removal etc.
                - Extract_Name = extracts the name of the player from the input string: returns a list of names tfidf
                - for each extracted name - query gets rephrased
            - genai = generates the content(code)
                - for each rephrased query - code for it gets generated
"""