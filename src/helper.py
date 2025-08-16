from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings


# extract text from a PDF file
def extract_text_from_pdf(data):
    loader = DirectoryLoader(
        data,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    documents = loader.load()
    return documents 


# remove all metadata from documents
def filter_docs(docs: List[Document]) -> List[Document]:
    """
    Filter out metadata.
    """
    minimal_docs: List[Document]  = []
    for doc in docs:
        src = doc.metadata.get('source')
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    'source': src}
            )
        )
    return minimal_docs


# create chunks of text
def split_text_into_chunks(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(minimal_docs)
    return chunks


# download embedding model from HuggingFace
def download_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings