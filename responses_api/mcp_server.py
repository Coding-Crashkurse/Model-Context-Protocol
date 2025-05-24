from typing import Dict, List, Tuple
from fastmcp import FastMCP

mcp = FastMCP("clothing_price_server") 

INVENTORY: Dict[str, float] = {
    "t-shirt": 19.99,
    "jeans":   59.90,
    "hoodie":  39.95,
}

def _normalize(item: str) -> str:
    return item.strip().lower()

def _item_exists(item: str) -> bool:
    return _normalize(item) in INVENTORY

@mcp.tool(description="Get the price of a clothing item; always returns (found, price)")
def get_price(item: str) -> Tuple[bool, float]:
    key = _normalize(item)
    return (_item_exists(key), INVENTORY.get(key, 0.0))

@mcp.tool(description="Add or update a clothing item with its price; always returns (item, price)")
def add_item(item: str, price: float) -> Tuple[str, float]:
    key = _normalize(item)
    INVENTORY[key] = max(price, 0.0)
    return key, INVENTORY[key]

@mcp.tool(description="List all clothing items with their prices")
def list_items() -> List[Tuple[str, float]]:
    return sorted(INVENTORY.items())

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=3000)
