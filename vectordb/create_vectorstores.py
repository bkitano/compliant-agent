from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from pathlib import Path
import os

doc_path = Path(__file__).parent / "docs/us-fcpa.txt"

loader = TextLoader(doc_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name='gtr-t5-large')
docsearch = FAISS.from_documents(texts, embeddings)

docsearch.save_local("vectorstores/us-fcpa-vectorstore")
