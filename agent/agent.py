import json
from dotenv import load_dotenv
from openai import OpenAI
from agent.tools import TOOLS, save_memory, search_web, invoke_model, create_notion_page


load_dotenv()

def agent(messages):

    # Initialize the OpenAI client
    client = OpenAI()

    # Make a ChatGPT API call with tool calling
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=TOOLS, # here we pass the tools to the LLM
        messages=messages
    )

    # Get the response from the LLM
    response = completion.choices[0].message

    messages.append(response)

    # Parse the response to get the tool call arguments
    if response.tool_calls:
        # Process each tool call
        for tool_call in response.tool_calls:
            # Get the tool call arguments
            tool_call_arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "save_memory":
                return save_memory(tool_call_arguments["memory"])
            elif tool_call.function.name == "web_search":
                search_results = search_web(tool_call_arguments["query"])
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"Here are the search results: {search_results}"})
                return invoke_model(messages)
            elif tool_call.function.name == "create_notion_page":
                create_notion_page(tool_call_arguments["page_title"], tool_call_arguments["markdown_content"])
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"Page {tool_call_arguments['page_title']} created successfully"})
                return invoke_model(messages)
    else:
        return response.content