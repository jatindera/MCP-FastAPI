"""
This example shows how to run the MCP server and the FastAPI app separately.
You can create an MCP server from one FastAPI app, and mount it to a different app.
"""
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class GreetRequest(BaseModel):
    name: str

class AddRequest(BaseModel):
    num1: float
    num2: float

@app.post("/greet", operation_id="greet_user_by_name")
async def greet(request: GreetRequest):
    """Greet the user with a personalized message."""
    return JSONResponse(content={"message": f"Hellooo {request.name}"})

@app.post("/add", operation_id="add_two_numbers")
async def add_numbers(request: AddRequest):
    """Add two numbers and return the result."""
    result = request.num1 + request.num2
    return JSONResponse(content={"result": result})

# Take the FastAPI app only as a source for MCP server generation
mcp = FastApiMCP(
    app,
    name = "MCP using FastAPI and React",
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