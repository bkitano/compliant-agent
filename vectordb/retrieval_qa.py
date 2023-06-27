from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import BaseLLMOutputParser
from langchain import PromptTemplate, LLMChain
from commons import chat_model
import xmltodict

embeddings = HuggingFaceEmbeddings(model_name="gtr-t5-large")
vectorstore = FAISS.load_local("vectorstores/us-fcpa-vectorstore", embeddings)

prompt_template = """You are given a proposed action, as well as relevant legal context that pertains to the legality of that proposed action.
Use the following pieces of legal context to help determine whether the proposed action is compliant with the law.
If the proposed action is compliant with the law, answer "YES". If the proposed action is not compliant with the law, answer "NO", and provide an explanation for your answer in the <reason></reason> section.

Think step-by-step BEFORE answering the question.

FORMAT:
```xml
<response>
    <step_by_step>
        <step>OBSERVATION</step>
        <step>OBSERVATION</step> (can have up to 5 observations)
    </step_by_step>
    <compliance_status>TRUE|FALSE</compliance_status>
    <reason>REASON</reason>
</response>
```

Format notes:
- you MUST close the <step> tag after each observation with a </step> tag

Examples (non-compliant):
PROPOSED ACTION:
I want to buy wine for my friend Steve for his 20th birthday.

CONTEXT:
It’s a crime to sell, deliver or give away alcoholic beverages to a person under the age of 21. As the licensee, you are subject to disciplinary action by the Authority whether you or your employee served the minor. It does not matter whether you thought the person was 21, if they lied about their age, or if they appeared to be at least 21 years old.

ANSWER:
<response>
    <step_by_step>
        <step key="1">Does the context closely relate to the proposed action? Yes.</step>
        <step key="2">Is the proposed action to buy alcohol for a friend? Yes.</step>
        <step key="3">Is the friend under the age of 21? Yes.</step>
        <step key="4">Is it a crime to sell, deliver or give away alcoholic beverages to a person under the age of 21? Yes.</step>
        <step key="5">Is the proposed action compliant with the law? No.</step>
    </step_by_step>
    <compliance_status>FALSE</compliance_status>
    <reason>It is a crime to sell, deliver or give away alcoholic beverages to a person under the age of 21.</reason>
</response>

Example (compliant):
PROPOSED ACTION:
I want to buy soda.

CONTEXT:
(a)Purposes
The purposes of a liquidation proceeding under this chapter shall be—
(1)as promptly as possible after the appointment of a trustee in such liquidation proceeding, and in accordance with the provisions of this chapter—
(A)to deliver customer name securities to or on behalf of the customers of the debtor entitled thereto as provided in section 78fff–2(c)(2) of this title; and
(B)to distribute customer property and (in advance thereof or concurrently therewith) otherwise satisfy net equity claims of customers to the extent provided in this section;

ANSWER:
<response>
    <step_by_step>
        <step key="1">Does the context closely relate to the proposed action? No.</step>
        <step key="2">Is the proposed action compliant with the law? Yes.</step>
    </step_by_step>
    <compliance_status>TRUE</compliance_status>
</response>

PROPOSED ACTION:
{query}

CONTEXT:
{context}

ANSWER:"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "query"])
chain_type_kwargs = {"prompt": PROMPT}

regulations = LLMChain(llm=chat_model, prompt=PROMPT)

# for debugging
# print(PROMPT.format(query=query, context=regs))#docs[0].page_content))#, context=d))
# print(regulations.run(query=query, context=regs))


def query_action_in_db(query):
    docs = vectorstore.similarity_search(query)
    docs_string = "\n\n".join([doc.page_content for doc in docs])
    return regulations.run(query=query, context=docs_string)



regulations_tool = Tool(
    name="Regulations DB",
    func=query_action_in_db,
    description="""Useful for when you need to check the legality or compliance of a specific action. The tool takes in a proposed action and returns whether or not the action is compliant.

    The format of the output is:
    <response>
        <step_by_step>
            <step>OBSERVATION</step>
            <step>OBSERVATION</step> (can have any number of observations)
        </step_by_step>
        <compliance_status>TRUE|FALSE</compliance_status>
        <reason>REASON</reason>
    </response>

    If an action's compliance status is FALSE, it requires the agent to use the "Exit Tool", and pass the reason to the Exit Tool as to which rules the action is in violation of.""",
)
