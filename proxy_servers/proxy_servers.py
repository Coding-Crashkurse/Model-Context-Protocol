# modern_proxy_server.py
import asyncio
from fastmcp import FastMCP, Client
from fastmcp.client.transports import SSETransport, StreamableHttpTransport

# KORRIGIERTE URL für das SSE-Backend:
# Normalerweise lauscht der SSE-Transport von FastMCP direkt auf /sse
# oder auf einem Pfad, der in der Serverkonfiguration unter sse_path angegeben ist.
# Wenn der legacy_backend_mcp.name = "LegacySSEBackend" ist und kein expliziter sse_path,
# dann ist der wahrscheinlichste Pfad /sse oder /LegacySSEBackend/sse,
# aber oft ist es einfach der Basis-URL + /sse.
# Wir nehmen an, dass der Standardpfad für den SSE-Transport /sse ist.
LEGACY_SSE_BACKEND_URL = "http://127.0.0.1:9001/sse" # !!! KORREKTUR: /sse statt /mcp/sse !!!

async def create_modern_proxy_instance() -> FastMCP | None:
    print(f"Attempting to create modern proxy for LEGACY SSE backend at: {LEGACY_SSE_BACKEND_URL}")

    try:
        legacy_backend_client = Client(
            transport=SSETransport(url=LEGACY_SSE_BACKEND_URL)
        )
    except NameError:
        print("FEHLER: SSETransport nicht gefunden. Stelle sicher, dass die Transportklassen korrekt importiert sind.")
        return None
    except Exception as e:
        print(f"FEHLER beim Erstellen des SSETransport für das Backend: {e}")
        return None

    try:
        print(f"Calling FastMCP.from_client with SSE client for {LEGACY_SSE_BACKEND_URL}...")
        
        modern_proxy_mcp = FastMCP.from_client(
            legacy_backend_client,
            name="ModernProxyToLegacy",
            stateless_http=True
        )
        
        tools_on_proxy = await modern_proxy_mcp.get_tools() 
        if not tools_on_proxy:
             print(f"WARNUNG: Proxy '{modern_proxy_mcp.name}' wurde erstellt, aber keine Tools vom Legacy SSE Backend übernommen.")
        else:
            print(f"Proxy '{modern_proxy_mcp.name}' erstellt. Geproxyte Tools vom SSE Backend: {list(tools_on_proxy.keys())}")
        return modern_proxy_mcp

    except Exception as e:
        print(f"FEHLER beim Erstellen des Proxys mit FastMCP.from_client() für SSE Backend: {e}")
        print(f"Details: {type(e)}, {e.args}")
        print(f"Stelle sicher, dass der Legacy SSE Backend-Server unter {LEGACY_SSE_BACKEND_URL} läuft.")
        return None

def main():
    print("Initializing Modern Proxy (will offer StreamableHTTP, consume SSE)...")
    proxy_mcp_instance = asyncio.run(create_modern_proxy_instance())

    if proxy_mcp_instance:
        proxy_host = "127.0.0.1"
        proxy_port = 8000
        print(f"Proxy instance created. Starting Modern Proxy Server ({proxy_mcp_instance.name}) on http://{proxy_host}:{proxy_port}/mcp (offering StreamableHTTP)")
        
        proxy_mcp_instance.run(
            transport="streamable-http",
            host=proxy_host,
            port=proxy_port
        )
    else:
        print("Moderner Proxy-Server konnte nicht gestartet werden.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nModern Proxy server (StreamableHTTP) shutting down.")
    except RuntimeError as e:
        if "Already running asyncio" in str(e):
            print(f"Laufzeitfehler: {e}")
        else:
            print(f"Ein unerwarteter Laufzeitfehler ist aufgetreten: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")