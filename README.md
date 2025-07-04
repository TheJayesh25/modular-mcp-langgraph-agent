# 🧠 LangGraph + MCP Agent: Summarize → Extract → Translate

This project demonstrates a modular AI agent built using [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain MCP](https://github.com/langchain-ai/langchain/tree/main/libs/mcp), capable of performing the following operations on any user-provided text:

1. **Summarize**: Reduces the length of the input while retaining key meaning.
2. **Extract Keywords**: Pulls out relevant keywords from text.
3. **Translate**: Translates input or extracted content into any specified language.

All functionalities are implemented as **MCP tools**, and invoked via a streaming **LangGraph agent**.

---

## 📁 Project Structure

```bash
langgraph-mcp-tool/
│
├── mcp_servers/
│ └── text_server.py # MCP tool server (summarize, extract_keywords, translate)
├── client.py # Async client: loads tools and runs LangGraph agent
├── graph.py # Defines the LangGraph agent and tool integration
├── config.py # Loads & resolves MCP server config with environment variables
├── mcp_config.json # MCP server configuration (tool -> server mapping)
├── .env # Stores your OpenAI API key
└── README.md # You're here!
```


---

## 🚀 Features

- **LangGraph agent**: Orchestrates tool use with tool-conditional routing.
- **Streaming output**: Agent messages stream token-by-token as the response is generated.
- **OpenAI GPT-4o**: Each tool uses OpenAI API internally for smart processing.
- **TextContent** output: MCP tool outputs use `TextContent`, converted seamlessly into `ToolMessage`.

---

## 🧠 How It Works

### MCP Server: `text_server.py`

The server exposes 3 tools via MCP using the `@mcp.tool()` decorator:

- `summarize(text: str)`: Uses GPT-4o to reduce input size.
- `extract_keywords(text: str)`: Extracts ~5–10 relevant keywords.
- `translate(text: str, language: str)`: Translates text to a target language.

These tools return:

```python
[TextContent(type="text", text="...")]
```
Which LangGraph understands and renders as ToolMessage content.

---

## Agent Execution: client.py
The client does the following:
1. Loads the MCP config from mcp_config.json.
2. Connects to the MCP text server using MultiServerMCPClient.
3. Loads the tools using load_mcp_tools.
4. Creates a LangGraph agent using those tools.
5. Runs an interactive prompt where user input is handled via:
- HumanMessage
- AgentState → LangGraph graph → streamed AI output
Handles exit / quit gracefully with os._exit(0) to avoid async cleanup bugs.

---

## LangGraph Agent: graph.py
The agent is built with:
- AgentState: Holds the full message history.
- ToolNode(tools): Registers all loaded MCP tools.
- tools_condition: Routes model output to tool nodes only when a tool is invoked.
- MemorySaver: Enables short-term memory for chat history.

---

## Config: config.py + mcp_config.json
- mcp_config.json defines how to run each MCP server (tool name → path).
- config.py resolves any ${ENV} variables and loads the JSON into Python.

Example mcp_config.json:
```
{
  "text": {
    "command": "python",
    "args": ["./mcp_servers/text_server.py"],
    "transport": "stdio"
  }
}
```

## 🧪 How to Run
### 1. Install dependencies
```bash
pip install -r requirements.txt
```
Make sure you have:
- Python 3.10+
- OpenAI SDK
- LangGraph
- LangChain MCP

### 2. Set up your .env
```bash
OPENAI_API_KEY=your-key-here
```

### 3. Run the agent
```bash
python agent/client.py
```

✅ You’ll see something like:
```
Loaded tools: ['summarize', 'extract_keywords', 'translate']
USER:
```

---


## 💬 Example Conversation
```
USER: Translate this sentence to Korean and then to Hindi: my name is Soham and I am 10 years old
ASSISTANT:
- Korean: 제 이름은 소함이고 10살입니다.
- Hindi: मेरा नाम सोहम है और मैं 10 साल का हूँ।

USER: Summarize this then: [long paragraph]
ASSISTANT: [Summary]

USER: Extract keywords from the text you just summarized
ASSISTANT: [Keywords]

USER: Translate each keyword to Japanese
ASSISTANT: [Translated keywords]
```

---

## 🧩 Extending This Project
- Add more MCP tools: sentiment analysis, grammar correction, text-to-speech
- Use LangGraph conditional logic for tool chaining
- Build a Streamlit front-end
- Store message history in a DB

---


### 🧑‍💻 Author
Jayesh Suryawanshi
- 🧠 Python Developer | 💡 AI Tools Builder | 🌍 Data & Engineering Enthusiast
- 📫 [LinkedIn](https://www.linkedin.com/in/jayesh-suryawanshi-858bb21aa/)
---
### 📃 License
MIT License
