import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage
from langchain_openai.chat_models.base import ChatOpenAI

from config import Config


def run_structured_with_errors(messages, llm, output_model):
    for _ in range(3):
        res = llm.with_structured_output(output_model, include_raw=True).invoke(messages)
        if res["parsed"]:
            return res["parsed"]
        messages.extend(
            [
                res["raw"],
                ToolMessage(
                    content=f'Respond by calling the function correctly. Exceptions found:\n\n{res["parsing_error"]}',
                    tool_call_id=res["raw"].tool_calls[0]["id"],
                ),
            ]
        )
    raise ValueError("Failed to extract")


class GptModels:

    def __init__(self):
        load_dotenv()
        self.langsmith_project = os.getenv("LANGCHAIN_PROJECT")
        self._gpt_4_turbo = None
        self._gpt_4_omni = None
        self._azure_llm = None
        self._claude_3 = None
        self.config = Config()

    @property
    def gpt_4_turbo(self):
        if self._gpt_4_turbo is None:
            self._gpt_4_turbo = ChatOpenAI(model=self.config.gpt_4_turbo, temperature=0.6)
        return self._gpt_4_turbo

    @property
    def gpt_4_omni(self) -> BaseChatModel:
        if self._gpt_4_omni is None:
            self._gpt_4_omni = ChatOpenAI(model=self.config.gpt_40, temperature=0)
        return self._gpt_4_omni

    @property
    def claude_3(self) -> BaseChatModel:
        if self._claude_3 is None:
            self._claude_3 = ChatAnthropic(model='claude-3-5-sonnet-20240620', max_tokens=4096, temperature=0)
        return self._claude_3
