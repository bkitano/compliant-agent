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
    func=lambda x: f"this is compliant behavior: {x}",
    description="Useful for when you need to check the legality of a specific action.",
    verbose=True,
)

mock_amazon_tool = Tool(
    name="Amazon Tool",
    func=lambda x: f"going to buy a gift on Amazon: {x}",
    description="Useful for when you need to buy a gift on Amazon.",
    verbose=True,
)

agent = ConversationalAgent.from_llm_and_tools(
    llm=chat_model,
    tools=[mock_compliance_tool, mock_amazon_tool],
    prefix=prefix,
    input_variables=["input", "agent_scratchpad", "chat_history"],
    verbose=True,
)
loaded_mem = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[mock_compliance_tool, mock_amazon_tool],
    memory=loaded_mem,
    verbose=True,
)
