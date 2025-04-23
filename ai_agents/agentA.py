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
    ) as mcp_server_tools:
        trace_id = gen_trace_id()
        with trace(workflow_name="Status_Demo", trace_id=trace_id):

            japan_agent = Agent(
                name="japan_agent",
                model="gpt-4o-mini",
                instructions="use appropriate tool to translate the status from Japanese to English and express the output in clearly in a well-written status update. Send two letters Language format for to and from as parmater alognwith the status text",
                # instructions="Convert the status from Japanese to English and Hindi and express it clearly in a well-written status update. Send two letters Language format for to and from as parmater alognwith the status text",
                mcp_servers=[mcp_server_tools],
                model_settings=ModelSettings(tool_choice="required")
            )
            input_text = input("Enter your status in Japnese: ")
            result = Runner.run_streamed(
                starting_agent=japan_agent,
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

