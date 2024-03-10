def extract_name(user):
    y = tf.transform([user])
    similarities = cosine_similarity(tf.transform(players_data), y)
    names_6 = []

    names_45 = []
    for i,s in enumerate(similarities):
        if(s>0.6):
            if(i not in names_6):
                names_6+=[players_data[i]]
        elif(s>0.40):                         # checking with 0.40 prob score
            if(i not in names_45):
                names_45+=[players_data[i]]
    return names_45 if len(names_6)==0 else names_6

## Preprocessing the Questions to reduce the search space and
def preprocess(text='How many runs did virat ,ishant, rohit scored in 2019'):
    # Remove Leading Blank Spaces
    text = text.strip()
    # Lower Case
    text = text.lower()
    #removing special characters and punctuations
    text = re.sub(r"[^a-zA-Z0-9.\s]+", '', text)
    #tokenize
    text = nltk.tokenize.word_tokenize(text)
    #stopwords
    final_text = []
    for i in text:
        if(i not in stop):
            final_text+=[i]
    return final_text

## REPHRASING THE QUESTION FOR DIFFERENT POSSIBLE PLAYER NAME
def rephrase(text,comparison=0):
    text = text.lower()
    rephrases = []
    preprocessed = preprocess(text)
    if(comparison==0):
        for i in preprocessed:
            one = extract_name(i)
            if len(one)!=0:
                if(len(one)==1):
                    text = re.sub(i,one[0],text)
                else:
                    for j in one:
                        rephrases+=[re.sub(i,j,text)]
        return [text] if(len(rephrases)==0) else rephrases
    else:
        final = []
        for i in preprocessed:
            one=extract_name(i)
            if(len(one)!=0):
                final+=[one]
        return final
                            
## MODEL ---- QUERY
def query_sql(code,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(code)
    rows = cur.fetchall()
    conn.close()
    return rows

def genai(prompt,question):
    output=model.generate_content([prompt,question])
    return output

def output(question):
    question=rephrase(question.lower())
    out=[]
    for i in question:
        out+=[genai(prompt,i).text]
    with open("test.sql", "w") as f:
        for i in out:
            f.write(re.sub('```','',re.sub('```sql','',i)))
    with open('test.sql', 'r') as sql_file:
        sql_commands = sql_file.read().split(';')
    return sql_commands