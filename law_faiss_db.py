from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.tools import Tool
from commons import llm_model
from pathlib import Path

doc_path = Path(__file__).parent / "docs/uk-bribery-act.txt"

loader = TextLoader(doc_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

#embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name='gtr-t5-large')
docsearch = FAISS.from_documents(texts, embeddings)#, collection_name="regulations")

docsearch.save_local("vectorstores/uk-bribery-act-vs")
#vectorstore = FAISS.load_local("data/CFR_vectorstore", embeddings)

regulations = RetrievalQA.from_chain_type(
    llm=llm_model, chain_type="stuff", retriever=docsearch.as_retriever()
)


regulations_tool = Tool(
    name="Regulations DB",
    func=regulations.run,
    description="Useful for when you need to find a specific regulation.",
)
