import json
import sys
from pathlib import Path

from Agents import LiteLlmAgent
from Services import ToolsService, ContextWindowService

sys.path.append(str(Path(__file__).parent))

tools_service = ToolsService()
context_window_service = ContextWindowService()
lite_llm_agent = LiteLlmAgent(
    model="gpt-4o",
    api_key="OPEN_AI_API_KEY",
    context_window_service=context_window_service,
    tools_service=tools_service,
)

MAX_QUESTIONS = 10
MAX_TOOL_CALLS = 10

question_count = 0
tool_call_count = 0

print("For exit the converzation write: 'exit'")

while question_count < MAX_QUESTIONS:
    message: str = input("Insert message: ")
    if not message.strip():
        print("Message is empty.")
        break

    if message.strip().lower() == "exit":
        sys.exit(0)

    question_count += 1
    context_window_service.add_to_conversation(role="user", message=message)

    response = lite_llm_agent.create_call()

    finish_reason = response.choices[0].finish_reason
    content = response.choices[0].message.content
    tool_calls = response.choices[0].message.tool_calls

    if content is not None:
        print("AGENT:")
        print(content)
        context_window_service.add_to_conversation(role="assistant", message=content)

    if tool_calls is not None and finish_reason == "tool_calls":
        if tool_call_count >= MAX_TOOL_CALLS:
            print(f"Maximum tool call reach ({MAX_TOOL_CALLS}).")
            break

        tool_call = tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        tool_id = tool_call.id

        tool = tools_service.get_tool(tool_name=function_name)
        if tool is None:
            print(f"Tool '{function_name}' not exists.")
            break

        function_response = tool(**function_args)
        tool_call_count += 1

        context_window_service.add_assistant_tool_call(
            tool_id=tool_id,
            function_name=function_name,
            function_args=function_args,
        )

        context_window_service.add_tool(
            tool_id=tool_id,
            function_name=function_name,
            function_response=function_response,
        )

        tool_response = lite_llm_agent.create_call()
        second_content = tool_response.choices[0].message.content

        if second_content:
            print("AGENT:")
            print(second_content)
            context_window_service.add_to_conversation(role="assistant", message=second_content)