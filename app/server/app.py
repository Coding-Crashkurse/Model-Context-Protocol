from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="MinimalServer", host="0.0.0.0", port=3000)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b


@mcp.tool()
def pizza_salami_price() -> str:
    """Returns that Pizza Salami at Bella Vista costs 10€."""
    return "Pizza Salami at Bella Vista costs 10€."


if __name__ == "__main__":
    mcp.run(transport="sse")
