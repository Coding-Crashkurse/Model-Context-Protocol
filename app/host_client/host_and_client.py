import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Global dictionary for registered servers.
servers_config: Dict[str, dict] = {}


class ServerRegistration(BaseModel):
    name: str
    url: str


class AskPayload(BaseModel):
    question: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the persistent client based on the initial servers_config.
    persistent_client = MultiServerMCPClient(servers_config)
    await persistent_client.__aenter__()
    app.state.persistent_client = persistent_client
    yield
    # On shutdown, gracefully close the persistent client.
    await app.state.persistent_client.__aexit__(None, None, None)


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/servers")
def list_servers():
    return servers_config


@app.post("/api/servers")
async def register_server(reg: ServerRegistration):
    # Add the new server to the configuration.
    servers_config[reg.name] = {"transport": "sse", "url": reg.url}
    # Reinitialize the persistent client to include the new server.
    if hasattr(app.state, "persistent_client"):
        await app.state.persistent_client.__aexit__(None, None, None)
    new_client = MultiServerMCPClient(servers_config)
    await new_client.__aenter__()
    app.state.persistent_client = new_client
    return {"status": "ok"}


@app.post("/api/ask")
async def ask_question(payload: AskPayload):
    model = ChatOpenAI(model="gpt-4o-mini")
    if servers_config:
        try:
            persistent_client = app.state.persistent_client
            tools = persistent_client.get_tools()
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({"messages": payload.question})
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during agent invocation: {str(e)}"
            )
    else:
        agent = create_react_agent(model, [])
        response = await agent.ainvoke({"messages": payload.question})
    answer_text = response.get("messages", "No answer received.")
    return {"answer": answer_text}
