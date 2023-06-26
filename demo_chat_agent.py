from langchain.agents import ConversationalAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from commons import chat_model
from langchain.agents import Tool

"""
This is a custom conversational chat agent. We are going to
modify the prefix and agent format instructions to ensure that 
it assesses the compliance of a prposed action.
"""

prefix = """
"""

mock_compliance_tool = Tool(
    name="Compliance Agent",
    func=lambda x: "this is not compliant behavior",
    description="Useful for when you need to check the legality of a specific action.",
)

agent = ConversationalAgent.from_llm_and_tools(
    llm=chat_model,
    tools=[mock_compliance_tool],
    prefix=prefix,
    input_variables=["input", "agent_scratchpad", "chat_history"],
    verbose=True,
)
loaded_mem = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[mock_compliance_tool],
    memory=loaded_mem,
    verbose=True,
)
