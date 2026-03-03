import asyncio
from urllib import response
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage

llm = ChatOllama(model = "mistral:latest")


SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "C:/Users/user/Desktop/MCP_client/.venv/Scripts/fastmcp.exe",
        "args": [
            "run",
            "main.py"
        ]

    }
}

async def main():
    print("Starting MultiServerMCPClient with servers:", list(SERVERS.keys()))
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    
    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    llm_with_tools = llm.bind_tools(tools)
    prompt = "What is 5 multiplied by 3?"
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", []):
        print("Response:", response)
        return

    print(f"\nLLM Response: {response}")
    print(f"Tool calls: {response.tool_calls}")
    
    selected_tool = response.tool_calls[0]["name"]
    selected_tool_args = response.tool_calls[0]["args"]
    selected_tool_id = response.tool_calls[0]["id"]

    print(f"\nSelected tool: {selected_tool}")
    print(f"Selected tool args: {selected_tool_args}")

    tool_result = await named_tools[selected_tool].ainvoke(selected_tool_args)
    print(f"\nTool result: {tool_result}")

    tool_message = ToolMessage(content=str(tool_result), tool_call_id=selected_tool_id)

    final_response = await llm_with_tools.ainvoke([prompt, response, tool_message])
    print(f"\nFinal response: {final_response}")

if __name__ == "__main__":
    asyncio.run(main())
