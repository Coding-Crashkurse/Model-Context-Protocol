import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

# Client-Logik
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

app = FastAPI()

# Statisches Verzeichnis anbinden
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-Memory Konfiguration der registrierten Server
servers_config: Dict[str, dict] = {}


class ServerRegistration(BaseModel):
    name: str
    url: str


class AskPayload(BaseModel):
    question: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/servers")
def list_servers():
    return servers_config


@app.post("/api/servers")
def register_server(reg: ServerRegistration):
    # Beispielhaft immer 'sse' als Transport
    servers_config[reg.name] = {"transport": "sse", "url": reg.url}
    return {"status": "ok"}


@app.post("/api/ask")
async def ask_question(payload: AskPayload):
    """Nutzt das LLM mit Tools (falls Server eingetragen) oder
    ohne Tools (falls keine Server vorhanden)."""

    # Minimales Chat-Modell
    model = ChatOpenAI(model="gpt-4o-mini")

    # Wenn es eingetragene MCP-Server gibt, holen wir deren Tools,
    # sonst erstellen wir den Agent ohne Tools.
    if servers_config:
        async with MultiServerMCPClient(servers_config) as client:
            tools = client.get_tools()
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({"messages": payload.question})
    else:
        # Kein Server => keine Tools
        agent = create_react_agent(model, [])
        response = await agent.ainvoke({"messages": payload.question})

    answer_text = response.get("messages", "Keine Antwort erhalten.")
    return {"answer": answer_text}
