import json
import asyncio
import gradio as gr
from openai import OpenAI

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


# ===== 大模型配置 =====
client = OpenAI(
    api_key="sk-b452b3933d4144fb851656983fe55077",
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-chat"


async def ask_ai(user_text):

    server = StdioServerParameters(
        command="python",
        args=["test.py"]
    )

    async with stdio_client(server) as (read, write):
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

            messages = [
                {"role": "user", "content": user_text}
            ]

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tool_defs,
                tool_choice="auto"
            )

            msg = response.choices[0].message

            # AI决定调用工具
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

                # 再让AI组织自然语言回答
                final = client.chat.completions.create(
                    model=MODEL,
                    messages=messages
                )

                return final.choices[0].message.content

            else:
                return msg.content


def chat(user_text):
    return asyncio.run(ask_ai(user_text))


demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="请输入问题"),
    outputs=gr.Textbox(label="AI回答"),
    title="MCP 智能助手",
    description="可聊天、可调用工具"
)

demo.launch()