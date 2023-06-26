from langchain.agents import ConversationalAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from commons import chat_model, llm_model
from langchain.agents import Tool

"""
This is a custom conversational chat agent. We are going to
modify the prefix and agent format instructions to ensure that 
it assesses the compliance of a prposed action.
"""

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

```
Thought: Do I need to use a tool? (Yes|No)
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I can now respond to the user with the completed action or observation.
Final Response: the final response to the original input message
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```"""

mock_compliance_tool = Tool(
    name="Compliance Agent",
    func=lambda x: f"this is compliant behavior: {x}",
    description="Useful for when you need to check the legality of a specific action.",
    verbose=True,
)

mock_amazon_tool = Tool(
    name="Amazon Tool",
    func=lambda x: f"Successfully purchased a gift on Amazon: {x}",
    description="Useful for when you need to buy a gift on Amazon. The input should be the name of the gift. It will send out an order request for that gift to Amazon.",
    verbose=True,
)

agent = ConversationalAgent.from_llm_and_tools(
    llm=llm_model,
    tools=[mock_compliance_tool, mock_amazon_tool],
    format_instructions=FORMAT_INSTRUCTIONS,
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
