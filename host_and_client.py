import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI


async def main():
    model = ChatOpenAI(model="gpt-4o-mini")
    servers_config = {
        "pizzaserver": {
            "transport": "sse",
            "url": "http://127.0.0.1:3000/sse",
        }
    }
    async with MultiServerMCPClient(servers_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        r = await agent.ainvoke({"messages": "What food does Bella Vista offer?"})
        print(r["messages"])


if __name__ == "__main__":
    asyncio.run(main())
