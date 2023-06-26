from langchain.chat_models import ChatAnthropic
from langchain.llms import Anthropic
import os

chat_model = ChatAnthropic(
    temperature=0,
    model="claude-v1.3-100k",
    anthropic_api_key=os.environ.get(
        "ANTHROPIC_API_KEY",
        "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",
    ),
)
llm_model = Anthropic(
    temperature=0,
    model="claude-v1.3-100k",
    anthropic_api_key=os.environ.get(
        "ANTHROPIC_API_KEY",
        "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",
    ),
)
