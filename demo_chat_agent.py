from langchain.agents import ConversationalAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from commons import chat_model
from compliance_agent import mock_compliance_tool

"""
This is a custom conversational chat agent. We are going to
modify the prefix and agent format instructions to ensure that 
it assesses the compliance of a prposed action.
"""

prefix = """
"""

agent = ConversationalAgent.from_llm_and_tools(
    llm=chat_model,
    tools=[mock_compliance_tool],
    prefix=prefix,
    input_variables=["input", "agent_scratchpad", "chat_history"],
)
loaded_mem = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[mock_compliance_tool],
    memory=loaded_mem,
)