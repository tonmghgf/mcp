import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():
    server = StdioServerParameters(
        command="python",
        args=["test.py"]
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("工具列表:")
            print(tools)

            result = await session.call_tool(
                "calculator",
                {
                    "a": 20,
                    "b": 5,
                    "operator": "*"
                }
            )

            print("结果:")
            print(result)


asyncio.run(main())