import os
from demo_chat_agent import agent_executor
from handler import AgentExecutorHandler

## if main:
if __name__ == "__main__":
    agent_executor_handler = AgentExecutorHandler("chat_session_id", "message_id")

    agent_executor.run(
        **{
            "input": "I want to buy a bottle of soda for my friend Steve.",
            "verbose": True,
            "callbacks": [agent_executor_handler],
        }
    )
