from openai.types.chat import ChatCompletionMessageParam
from typing import Literal
import json


class ContextWindowService:
    def __init__(self):
        self.conversation: list[ChatCompletionMessageParam] = []

    def get_conversation_context(self) -> list[ChatCompletionMessageParam]:
        return self.conversation

    def add_to_conversation(self, role: Literal["user", "assistant", "tool"], message: str):
        self.conversation.append({"role": role, "content": message})

    def add_user_message(self, message: str):
        self.conversation.append({"role": "user", "content": message})

    def add_tool(self, tool_id: str, function_name: str, function_response: str):
        self.conversation.append(
            {
                "role": "tool",
                "tool_call_id": tool_id,
                "name": function_name,
                "content": json.dumps(function_response),
            }
        )

    def add_assistant_tool_call(
            self,
            tool_id: str,
            function_name: Literal["get_dividend_date", "get_stock_price"],
            function_args
    ):
        self.conversation.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_id,
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args),
                    },
                }
            ]
        })
