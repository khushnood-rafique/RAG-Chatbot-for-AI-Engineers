from flask import Flask, render_template, request, jsonify
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
from src.prompt import *
from src.helper import download_embeddings
import os


app = Flask(__name__)


# Load environment variables
load_dotenv()

# Set up Pinecone and OpenAI API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# load the embedding model
embeddings = download_embeddings()

# Initialize Pinecone Index
index_name = "rag-chatbot-for-ai-engineers"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Create a retrieval chain
retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={"k": 3})


# Create a chat model
llm = ChatOllama(
    model="gemma3:12b",                    
    base_url="http://127.0.0.1:11434"
)

# prompt template for the chat model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)


# Create a question-answering chain
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)


# Define the Flask routes
@app.route('/get', methods=['GET','POST'])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response['answer'])
    return str(response['answer'])


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)