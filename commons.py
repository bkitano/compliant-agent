from langchain.chat_models import ChatAnthropic
from langchain.llms import Anthropic
import os

chat_model = ChatAnthropic(
    model="claude-v1.3-100k", anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]
)
llm_model = Anthropic(
    model="claude-v1.3-100k", anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]
)
