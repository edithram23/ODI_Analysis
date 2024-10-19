from sentence_transformers import SentenceTransformer
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import numpy as np
import faiss
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv('API.env')
class rule():
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        file='ODI.pdf'
        loader = PyPDFLoader(file)
        raw_documents = loader.load() # Load the documents into a list
        self.text = ''
        for i in raw_documents:
            self.text+=i.page_content
        text_splitter = RecursiveCharacterTextSplitter(
                        # Set a really small chunk size, just to show.
                        chunk_size=512,
                        chunk_overlap=64
                    )
        documents = text_splitter.create_documents([self.text])
        self.doc_texts = [doc.page_content for doc in documents]
        embeddings = self.model.encode(self.doc_texts, convert_to_tensor=False)
        embeddings = np.array(embeddings).astype('float32')

        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))

        ids = np.array(range(len(documents))).astype('int64')
        self.index.add_with_ids(embeddings, ids)
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        print("Documents indexed successfully!")
        
    def output(self,query):
        query_embedding = self.model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding).astype('float32')

        # Perform search to retrieve top 2 matching documents
        k = 10
        distances, indices = self.index.search(query_embedding, k)

        # Print the retrieved documents based on their indices
        out_text = ''
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Ensure the index exists
                out_text+=self.doc_texts[idx]
        return out_text
    
    def groq_output(self, query):
        user_query=query
        context = self.output(query)
        user_query=query
        print(context)
        prompt =  f'''You are a Chatbot expert in cricket and have been given a user query along with the  Cricket rules as context.
                    Please analyze the query and provide an accurate response based solely on the context provided.
                    =====================
                    User Query: {user_query}
                    Context: {context}
                    =====================
                    Guidelines:
                    - Analyze the user query in detail and provide an appropriate output based on the given context.
                    - If the query is not related to cricket, respond with "No Answer".
                    - Provide only information that is explicitly stated in the context.
                    - You are allowed to provide an explanation/reason for your decision, based on the context only if it was needed.
                    - Do not reference clause numbers, only provide relevant points.
                    - Keep the answer simple, straightforward, and avoid overcomplicating.
                    - Do not suggest like "on the ICC website".
                    - Beutify your output, keep it simple'''
        chat_completion = self.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-70b-versatile",
        )
        return chat_completion.choices[0].message.content.split("|")