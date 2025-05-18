import asyncio
from fastmcp import FastMCP, Client
from fastmcp.client.transports import SSETransport

LEGACY_SSE_BACKEND_URL = "http://127.0.0.1:9001/sse"

async def create_modern_proxy_instance() -> FastMCP | None:
    print(f"Attempting to create modern proxy for LEGACY SSE backend at: {LEGACY_SSE_BACKEND_URL}")

    try:
        legacy_backend_client = Client(
            transport=SSETransport(url=LEGACY_SSE_BACKEND_URL)
        )
    except NameError:
        print("ERROR: SSETransport not found. Ensure that the transport classes are imported correctly.")
        return None
    except Exception as e:
        print(f"ERROR creating SSETransport for the backend: {e}")
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
             print(f"WARNING: Proxy '{modern_proxy_mcp.name}' was created, but no tools were adopted from the Legacy SSE Backend.")
        else:
            print(f"Proxy '{modern_proxy_mcp.name}' created. Proxied tools from SSE Backend: {list(tools_on_proxy.keys())}")
        return modern_proxy_mcp

    except Exception as e:
        print(f"ERROR creating the proxy with FastMCP.from_client() for SSE Backend: {e}")
        print(f"Details: {type(e)}, {e.args}")
        print(f"Ensure that the Legacy SSE Backend server is running at {LEGACY_SSE_BACKEND_URL}.")
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
        print("Modern Proxy server could not be started.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nModern Proxy server (StreamableHTTP) shutting down.")
    except RuntimeError as e:
        if "Already running asyncio" in str(e):
            print(f"Runtime error: {e}")
        else:
            print(f"An unexpected runtime error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")