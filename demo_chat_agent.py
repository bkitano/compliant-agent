import os
from langchain import OpenAI
from langchain.agents import ConversationalAgent, Tool, AgentExecutor
from compliance_agent import compliance_tool
from langchain.memory import ConversationBufferMemory

"""
This is a custom conversational chat agent. We are going to
modify the prefix and agent format instructions to ensure that 
it assesses the compliance of a prposed action.
"""

prefix = """
"""

llm = OpenAI(
    temperature=0.7,
    streaming=True,  # this is required for the llm_on_new_token callback to work
    openai_api_key=os.environ["OPENAI_API_KEY"],
)

agent = ConversationalAgent.from_llm_and_tools(
    llm=llm,
    tools=[compliance_tool],
    prefix=prefix,
    input_variables=["input", "agent_scratchpad", "chat_history"],
)
loaded_mem = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[compliance_tool],
    memory=loaded_mem,
)