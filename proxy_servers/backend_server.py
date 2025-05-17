# legacy_backend_server.py
from fastmcp import FastMCP

# Erstelle den Legacy Backend-Server, der SSE anbietet
legacy_backend_mcp = FastMCP(
    name="LegacySSEBackend",
    # stateless_http ist für SSE implizit True
)

@legacy_backend_mcp.tool(description="Greets a person by name from the legacy SSE system.")
def greet_legacy(name: str) -> str:
    print(f"[LegacySSEBackend] Tool 'greet_legacy' called with name: {name}")
    return f"Greetings, {name}, from the ancient SSE Archives!"

@legacy_backend_mcp.tool(description="Provides a legacy data string.")
def get_legacy_data(request_id: int) -> str:
    print(f"[LegacySSEBackend] Tool 'get_legacy_data' called for ID: {request_id}")
    return f"LegacyDataString-{request_id}-SSEOrigin"

if __name__ == "__main__":
    backend_host = "127.0.0.1"
    backend_port = 9001 # Ein anderer Port für das Legacy-Backend
    print(f"Starting Legacy Backend Server ({legacy_backend_mcp.name}) on http://{backend_host}:{backend_port}/mcp (offering SSE)")
    legacy_backend_mcp.run(
        transport="sse", # !!! Wichtig: Dieses Backend läuft mit SSE !!!
        host=backend_host,
        port=backend_port
    )