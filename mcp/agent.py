import json
import asyncio
from openai import OpenAI

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


# ========= DeepSeek / OpenAI兼容接口 =========
client = OpenAI(
    api_key="sk-b452b3933d4144fb851656983fe55077",
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-chat"


# ========= MCP连接 =========
async def connect_mcp():
    server = StdioServerParameters(
        command="python",
        args=["test.py"]
    )

    return stdio_client(server)


# ========= 主逻辑 =========
async def main():

    async with await connect_mcp() as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools_data = await session.list_tools()

            tool_defs = []

            for t in tools_data.tools:
                tool_defs.append({
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": t.inputSchema
                    }
                })

            print("AI助手已启动，输入 exit 退出")

            messages = []

            while True:
                user_input = input("\n你：")

                if user_input.lower() == "exit":
                    break

                messages.append({
                    "role": "user",
                    "content": user_input
                })

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tool_defs,
                    tool_choice="auto"
                )

                msg = response.choices[0].message

                # 如果AI决定调用工具
                if msg.tool_calls:

                    for call in msg.tool_calls:
                        name = call.function.name
                        args = json.loads(call.function.arguments)

                        result = await session.call_tool(name, args)

                        tool_result = result.content[0].text

                        messages.append(msg)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": tool_result
                        })

                    # 再让AI总结输出
                    final = client.chat.completions.create(
                        model=MODEL,
                        messages=messages
                    )

                    answer = final.choices[0].message.content
                    print("AI：", answer)

                    messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:
                    answer = msg.content
                    print("AI：", answer)

                    messages.append({
                        "role": "assistant",
                        "content": answer
                    })


asyncio.run(main())