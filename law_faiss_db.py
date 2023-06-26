from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.tools import Tool
from commons import llm_model
from pathlib import Path

doc_path = Path(__file__).parent / "uk-bribery-act.txt"

loader = TextLoader(doc_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings, collection_name="regulations")

regulations = RetrievalQA.from_chain_type(
    llm=llm_model, chain_type="stuff", retriever=docsearch.as_retriever()
)

regulations_tool = Tool(
    name="Regulations DB",
    func=regulations.run,
    description="Useful for when you need to find a specific regulation.",
)
