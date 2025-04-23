"""
This example shows how to run the MCP server and the FastAPI app separately.
You can create an MCP server from one FastAPI app, and mount it to a different app.
"""
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from apis_tools import app
# Take the FastAPI app only as a source for MCP server generation
mcp = FastApiMCP(
    app,
    name = "MCP Implementation",
    describe_all_responses=True,
    describe_full_response_schema=True
    )

# Mount the MCP server to a separate FastAPI app
mcp.mount()

# Run the MCP server separately from the original FastAPI app.
# It still works 🚀
# Your original API is **not exposed**, only via the MCP server.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)