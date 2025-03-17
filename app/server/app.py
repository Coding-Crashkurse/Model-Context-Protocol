from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="MinimalServer", host="0.0.0.0", port=3000)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Addiert zwei Zahlen."""
    return a + b


@mcp.tool()
def pizza_salami_price() -> str:
    """Gibt zurück, dass Pizza Salami bei Bella Vista 10€ kostet."""
    return "Pizza Salami bei Bella Vista kostet 10€."


if __name__ == "__main__":
    # Start über SSE
    mcp.run(transport="sse")
