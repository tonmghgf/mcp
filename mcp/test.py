import os
from mcp.server.fastmcp import FastMCP

# 创建服务
mcp = FastMCP("FileSystem")


@mcp.tool()
def get_desktop_files() -> list:
    """获取当前用户桌面文件列表"""
    return os.listdir(os.path.expanduser("~/Desktop"))


@mcp.tool()
def calculator(a: float, b: float, operator: str) -> float:
    """
    基础计算器

    参数:
    operator: '+', '-', '*', '/'
    """
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        raise ValueError("无效运算符")


if __name__ == "__main__":
    mcp.run(transport="stdio")