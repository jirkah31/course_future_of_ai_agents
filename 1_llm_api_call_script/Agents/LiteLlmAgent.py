from Services import ToolsService, ContextWindowService
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class LiteLlmAgent:
    def __init__(
            self,
            model: str,
            api_key: str,
            context_window_service: ContextWindowService,
            tools_service: ToolsService
    ):
        self.__client = OpenAI(api_key=os.getenv(api_key))
        self.__model = model
        self.__context_window_service = context_window_service
        self.__tools_service = tools_service

    def create_call(self):
        return self.__client.chat.completions.create(
            model=self.__model,
            messages=self.__context_window_service.get_conversation_context(),
            tools=self.__tools_service.get_tools_list(),
            tool_choice="auto",
        )
