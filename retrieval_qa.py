from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain import PromptTemplate, LLMChain
from commons import chat_model

embeddings = HuggingFaceEmbeddings(model_name='gtr-t5-large')
vectorstore = FAISS.load_local("vectorstores/us-fcpa-vectorstore", embeddings)

query = "I want to bribe a foreign official with a $200 gift card to Amazon."
docs = vectorstore.similarity_search(query)
regs = ""
for i in range(len(docs)):
    regs += docs[i].page_content + '\n' + '\n'


prompt_template = """You are given a proposed action, as well as relevant legal context that pertains to the legality of that proposed action.
Use the following pieces of legal context to help determine whether the proposed action is compliant with the law.
If the proposed action is compliant with the law, answer "YES". If the proposed action is not compliant with the law, answer "NO", and provide an explanation for your answer. 

PROPOSED ACTION:
{query}

CONTEXT:
{context}

ANSWER:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "query"]
)
chain_type_kwargs = {"prompt": PROMPT}

regulations = LLMChain(llm=chat_model, prompt=PROMPT)

#for debugging
#print(PROMPT.format(query=query, context=regs))#docs[0].page_content))#, context=d))
#print(regulations.run(query=query, context=regs))

regulations_tool = Tool(
    name="Regulations DB",
    func=regulations.run(query=query, context=regs),
    description="Useful for when you need to find a specific regulation.",
)