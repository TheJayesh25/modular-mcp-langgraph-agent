
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, add_messages, START
from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from typing import List, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import BaseTool

class AgentState(BaseModel):
    messages: Annotated[List, add_messages]

def build_agent_graph(tools: List[BaseTool] = []):
    prompt = """
You are an assistant. You have access to the following tools:

{tools}

Respond to the user using natural language or JSON to call tools when necessary.
    """

    llm = ChatOpenAI(model="gpt-4o")
    if tools:
        llm = llm.bind_tools(tools)
        tool_docs = [tool.model_dump_json(include=["name", "description"]) for tool in tools]
        prompt = prompt.format(tools="\n".join(tool_docs))

    def agent_fn(state: AgentState) -> AgentState:
        response = llm.invoke([SystemMessage(content=prompt)] + state.messages)
        state.messages.append(response)
        return state

    graph = StateGraph(AgentState)
    graph.add_node("assistant", agent_fn)
    graph.add_node(ToolNode(tools))

    graph.add_edge(START, "assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")

    return graph.compile(checkpointer=MemorySaver())

