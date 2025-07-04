
import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient, load_mcp_tools
from langchain_core.messages import HumanMessage, AIMessageChunk
from graph import build_agent_graph, AgentState
from config import mcp_config
from typing import AsyncGenerator

async def stream_response(input, graph, config) -> AsyncGenerator[str, None]:
    async for chunk, _ in graph.astream(input=input, stream_mode="messages", config=config):
        if isinstance(chunk, AIMessageChunk):
            yield chunk.content

async def main():
    client = MultiServerMCPClient(connections=mcp_config)

    async with client.session("text") as session:
        tools = await load_mcp_tools(session)
        print("Loaded tools:", [tool.name for tool in tools])

        graph = build_agent_graph(tools)
        config = {"configurable": {"thread_id": "chat-1"}}

        while True:
            user = input("\n\nUSER: ")
            if user.lower() in ["quit", "exit"]:
                # sys.exit(0)
                break

            print("\nASSISTANT:\n")
            async for part in stream_response(
                AgentState(messages=[HumanMessage(content=user)]),
                graph,
                config
            ):
                print(part, end="", flush=True)
        
    # sys.exit(0)

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    try:
        asyncio.run(main())
    except:
        pass  # Ignore all errors during shutdown
    finally:
        import os
        os._exit(0)  # Force exit regardless of cleanup issues
