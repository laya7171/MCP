from __future__ import annotations
from fastmcp import FastMCP

mcp = FastMCP("Arith")

@mcp.tool
def _as_number(x):
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        return float(x)
    
    raise ValueError("Expected a number (int/float/str) or numeric string")

@mcp.tool
async def add(a: float, b: float)->float:
    """Returns the sum of a and b"""

    return _as_number(a) + _as_number(b)

@mcp.tool
async def subtract(a: float, b: float)->float:
    """Returns the difference of a and b"""

    return _as_number(a) - _as_number(b)

@mcp.tool 
def multiply(a: float, b: float)->float:
    """Returns the product of a and b"""

    return _as_number(a) * _as_number(b)

if __name__ == "__main__":
    mcp.run()
    

