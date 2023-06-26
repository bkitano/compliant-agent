import os
from demo_chat_agent import agent_executor
from handler import AgentExecutorHandler

## if main:
if __name__ == "__main__":
    agent_executor_handler = AgentExecutorHandler("chat_session_id", "message_id")

    agent_executor.run(
        **{
            "input": "I want to buy a bottle of alcohol for my friend Steve.",
            "callbacks": [
                # agent_executor_handler
                ],
        }
    )
    agent_executor.run(
        **{
            "input": "I want to buy a bottle of soda instead.",
            "callbacks": [
                # agent_executor_handler
                ],
        }
    )
