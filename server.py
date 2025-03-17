# app.py
from mcp.server.fastmcp import FastMCP
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from ingest import load_bellavista_documents

vectorstore = load_bellavista_documents()
embeddings = OpenAIEmbeddings()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

mcp = FastMCP("ServerWithPromptsResources", host="127.0.0.1", port=3000)


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b


@mcp.tool()
def search_docs(query: str) -> str:
    results = retriever.invoke(query)
    texts = []
    for i, doc in enumerate(results):
        texts.append(f"Document {i + 1}:\n{doc.page_content}")
    return "\n\n".join(texts)


@mcp.resource("resource://hello")
def resource_hello() -> str:
    return "Hello from the resource endpoint!"


@mcp.resource("resource://food/{item}")
def resource_food(item: str) -> str:
    if item.lower() == "pizza":
        return "Bella Vista's wood-fired pizza is priced at 10€."
    return "No details available for that item."


@mcp.prompt(name="friendly_greeting", description="Generates a short greeting message.")
def prompt_friendly_greeting(name: str) -> list[dict]:
    return [
        {"role": "assistant", "content": "You are a friendly helper."},
        {"role": "user", "content": f"Welcome, {name}! How can I assist you today?"},
    ]


if __name__ == "__main__":
    mcp.run(transport="sse")
