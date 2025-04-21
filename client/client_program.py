import asyncio
import os

from agents import Agent, Runner, gen_trace_id, set_default_openai_key, trace
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from dotenv import find_dotenv, load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console

console = Console()

load_dotenv(find_dotenv())

set_default_openai_key(os.getenv("OPENAI_API_KEY"))

async def main():
    # Initialize the MCP server with a context manager
    async with MCPServerSse(
        name="MCP using FastAPI and React",
        params={"url": "http://localhost:8000/mcp"},
        cache_tools_list=True,
    ) as greet_mcp_server:
        trace_id = gen_trace_id()
        with trace(workflow_name="mcp_demo", trace_id=trace_id):

            mcp_agent = Agent(
                name="mcp_agent",
                model="gpt-4o-mini",
                instructions="Based on the user input please choose the right tool. For example: if user enters name, use the greet tool. If user enters two numbers use add tool",
                mcp_servers=[greet_mcp_server],
                model_settings=ModelSettings(tool_choice="required")
            )
            while True:
                input_text = input("Enter your input: ")
                if input_text == "exit":
                    break

                result = Runner.run_streamed(
                    starting_agent=mcp_agent,
                    input=input_text,
                )

                print("\n")
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(
                        event.data, ResponseTextDeltaEvent
                    ):
                        console.print(event.data.delta, end="", highlight=False)
                print("\n")

if __name__ == "__main__":
    asyncio.run(main())

