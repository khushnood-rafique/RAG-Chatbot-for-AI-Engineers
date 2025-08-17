from dotenv import load_dotenv
import os
from src.helper import extract_text_from_pdf, filter_docs, split_text_into_chunks, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore


# Load environment variables
load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set environment variables for Pinecone and OpenAI API keys
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# extract text from PDF files in the 'data' directory
extracted_text_from_pdf = extract_text_from_pdf('data/')

# filter out metadata from the documents
minimal_docs = filter_docs(extracted_text_from_pdf)

# split the text into chunks
chunks = split_text_into_chunks(minimal_docs)

# download the embedding model
embeddings = download_embeddings()

# Initialize Pinecone
pinecone_api_key = PINECONE_API_KEY
pinecone_client = Pinecone(api_key=pinecone_api_key)

# create a Pinecone index
index_name = "rag-chatbot-for-ai-engineers"

if not pinecone_client.has_index(index_name):
    pinecone_client.create_index(
        name=index_name,
        dimension=384,  # Dimension of the embeddings
        metric="cosine",  # Similarity metric
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pinecone_client.Index(index_name)

# create a vector store using the text chunks and embeddings
docsearch = PineconeVectorStore.from_documents(
    documents=chunks,
    index_name=index_name,
    embedding=embeddings
)


