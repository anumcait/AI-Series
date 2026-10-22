# 🚀 Day 31 — Build a Local MCP-Powered AI Assistant 🔌🤖

## Objective

Build a local AI assistant using Python, Ollama, MCP (Model Context Protocol), and Streamlit. The assistant discovers tools, selects an appropriate tool based on a natural-language request, executes it, and explains the result.

## Tech Stack

- Python
- Ollama — `qwen3:4b`
- MCP Python SDK — `mcp`
- Streamlit
- Ollama Python library

## Project Structure

```
Day-31/
├── app.py
├── server.py
├── requirements.txt
└── workspace/
    └── README.md
```

## 1\. Environment Setup

Created and activated the existing Python virtual environment located at `../../venv`.

Installed dependencies using:

```
python -m pip install -r requirements.txt
```

**requirements.txt**

```
mcp>=1.28,<2
ollama
streamlit
```

Verified the installation:

```
python -c "import mcp, ollama, streamlit; print('All dependencies installed successfully')"
```

## 2\. MCP Server — `server.py`

Implemented a local MCP server using `FastMCP` with two read-only tools:

- `list_files()` — lists supported files inside the approved workspace.
- `read_file(path)` — reads supported text files using relative paths.

Safety measures include workspace path validation, restrictions on supported file extensions, symbolic-link checks, and file-size limits.

The server uses standard input/output (stdio) transport to communicate with the MCP client.

## 3\. AI Client — `app.py`

Implemented a Streamlit interface that:

1. Launches the MCP server as a local subprocess.
2. Initializes an MCP client session.
3. Discovers available tools using `session.list_tools()`.
4. Passes the discovered tool definitions to Ollama.
5. Lets the language model select a tool and generate arguments.
6. Executes the selected tool using `session.call_tool()`.
7. Sends the tool results back to the model for a natural-language explanation.
8. Displays the answer and MCP activity in the Streamlit interface.

The application uses `qwen3:4b` through Ollama's local API.

## 4\. Run the Application

Start the application from the Day-31 project directory:

```
python -m streamlit run app.py
```

Open the local address:

```
http://localhost:8501
```

## 5\. Implementation Test

**Prompt:** List all files in my project folder.

**Observed result:**

```
Approved workspace:
D:\AI-Series\Practice-Lab\Day-31\workspace

Your project folder contains 1 file:
README.md
```

The assistant successfully listed the existing `README.md` file in the approved workspace.

## How It Works in Real Time

```
User Question
     ↓
Streamlit Interface
     ↓
Ollama — Tool Selection
     ↓
MCP Client
     ↓
MCP Server
     ↓
Python Tool Execution
     ↓
Tool Result → Ollama
     ↓
Natural-Language Answer
```

The application discovers tools at runtime, executes requests against the local workspace, and displays the results. It starts a new MCP server session for each submitted question.

## Key Learnings

- MCP standardizes communication between AI applications and external tools.
- Tool discovery provides names, descriptions, and input schemas dynamically.
- The language model selects tools, while Python executes them.
- Tool results enable answers based on actual file contents.
- Read-only tools and workspace restrictions provide basic safety controls.

## Current Limitations

- Only file listing and text-file reading are implemented.
- Continuous monitoring and file modification are not supported.
- Human approval for write operations has not been implemented.
- Tool selection depends on the language model's reliability.

## Conclusion

Successfully installed the dependencies, implemented the local MCP server and Streamlit client, connected Ollama, and verified that the assistant could list files from the approved workspace.

### Screenshots
