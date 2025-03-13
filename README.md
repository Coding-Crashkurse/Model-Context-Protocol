# MCP (Model Context Protocol)

**MCP (Model Context Protocol)** is an open protocol by Anthropic that standardizes how LLM-powered applications communicate with external data sources and tools. It defines three main “primitives”:

- **Resources** (like GET endpoints, e.g., `resource://food/pizza`)
- **Tools** (functions callable by an LLM, e.g., `search_docs(query="...")`)
- **Prompts** (reusable conversation templates)

This repo shows multiple examples how to integrate servers and clients into AI Apps.

### Example Project Files:

- **`client_resource_langgraph.py`**:
  Extends `MultiServerMCPClient` into `MultiServerMCPClientWithResources`, allowing listing and reading MCP resources, demonstrated by a simple example.

- **`client_resource.py`**:
  Connects to an MCP server via SSE, lists available resources and prompts, reads a specific resource, and demonstrates retrieving a configured prompt.

- **`host_and_client.py`**:
  Uses the `MultiServerMCPClient` with a LangGraph agent. Loads tools from the MCP server and enables an LLM model (GPT-4o-mini) to autonomously invoke those tools (e.g., "What food does Bella Vista offer?").

- **`server.py`**:
  Sets up an MCP server accessible via SSE, defining tools (`add`, `multiply`, `search_docs`), resources (`resource://food/{item}`), and a prompt (`friendly_greeting`).
