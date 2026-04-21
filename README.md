# 一、项目介绍

本项目实现了一个完整的 AI Agent 系统，包含：

- MCP 服务端（提供工具能力）
- MCP 客户端（连接工具）
- 大模型（负责理解用户意图）
- Web 前端（聊天界面）

用户输入自然语言，例如：

```
帮我算 88 * 77
```

系统自动识别需要调用计算器工具，并返回：

```
88 × 77 = 6776
```

# 二、项目演示

## 聊天问答

```
你：你好
AI：你好，我是你的智能助手，请问有什么可以帮你？
```

## 工具调用：计算器

```
你：帮我算 66 * 88
AI：66 × 88 = 5808
```

## 工具调用：查看桌面文件

```
你：看看我桌面有什么文件
AI：你的桌面有以下文件：
1.txt
视频.mp4
工作资料
```

![01](.\图片\01.png)

# 三、系统架构

```
用户输入问题
    ↓
网页前端（Gradio）
    ↓
大模型理解问题
    ↓
判断是否调用工具
    ↓
MCP Client
    ↓
MCP Server（test.py）
    ↓
执行本地工具
    ↓
结果返回给大模型
    ↓
生成自然语言回复
    ↓
显示到网页
```

# 四、项目目录结构

```
D:\mcp\
├── test.py          # MCP 服务端（注册工具）
├── client.py        # 命令行客户端测试
├── app.py           # Web 聊天前端
├── README.md
```

# 五、环境要求

| 项目     | 要求                    |
| -------- | ----------------------- |
| Python   | 3.13+                   |
| 操作系统 | Windows / Linux / macOS |
| 网络     | 可访问模型 API          |
| 推荐环境 | Conda                   |

# 六、安装教程

## 1. 创建虚拟环境

```
conda create -n mcp python=3.13
conda activate mcp
```

## 2. 安装依赖

```
pip install mcp
pip install "mcp[cli]"
pip install openai
pip install gradio
```

国内镜像：

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio openai
```

# 七、配置模型 API

打开 `app.py`

找到：

```
client = OpenAI(
    api_key="你的API_KEY",
    base_url="https://api.deepseek.com"
)
```

修改为：

```
client = OpenAI(
    api_key="sk-xxxxxx",
    base_url="https://api.deepseek.com"
)
```

# 八、运行项目

```
python app.py
```

启动成功后访问：

```
http://127.0.0.1:7860
```

# 九、test.py（MCP 服务端说明）

该文件负责向 AI 提供本地工具能力。

## 示例工具1：查看桌面文件

```
@mcp.tool()
def get_desktop_files():
    return os.listdir(os.path.expanduser("~/Desktop"))
```

作用：

- 获取当前用户桌面所有文件名

## 示例工具2：计算器

```
@mcp.tool()
def calculator(a, b, operator):
```

支持：

```
+
-
*
/
```

# 十、前端 app.py 工作流程

## 用户输入：

```
帮我算 5*9
```

## AI 判断：

需要调用工具：

```
calculator
```

## MCP 执行：

```
calculator(5,9,"*")
```

## 返回：

```
45
```

## AI 总结输出：

```
5 × 9 = 45
```

# 十一、自定义工具开发

你可以继续扩展更多本地能力。

## 示例：读取 txt 文件

```
@mcp.tool()
def read_txt(path:str):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()
```

## 示例：创建文件夹

```
@mcp.tool()
def make_dir(name:str):
    os.mkdir(name)
    return "创建成功"
```

## 示例：打开浏览器

```
@mcp.tool()
def open_baidu():
    import webbrowser
    webbrowser.open("https://www.baidu.com")
```

# 十二、常见报错解决

## 1. No module named gradio

```
pip install gradio
```

## 2. No module named openai

```
pip install openai
```

## 3. MCPClient 导入失败

新版 SDK 已废弃旧写法。

使用：

```
from mcp.client.stdio import stdio_client
```

## 4. 页面打不开

访问：

```
http://127.0.0.1:7860
```

或关闭占用端口程序。