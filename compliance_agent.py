from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType, MRKLChain
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
from law_faiss_db import llm, regulations_tool

tools = [regulations_tool]

# todo: may want to customize the agent by constructing an
# agent executor and passing it to initialize_agent with
# custom prefix, suffix etc.
# MRKLChain.from_agent_and_tools(
#     llm,
#     tools,
#     prefix="",
#     suffix="",
#     verbose=True,
# )

# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

compliance_tool = Tool(
    name="Compliance Agent",
    func=agent.run,
    description="Useful for when you need to check the legality of a specific action.",
)
