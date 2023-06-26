from demo_chat_agent import agent_executor
import os

## if main:
if __name__ == '__main__':

    print(os.environ.get("ANTHROPIC_API_KEY"))

    # agent_executor.run("I want to buy a bottle of alcohol.")