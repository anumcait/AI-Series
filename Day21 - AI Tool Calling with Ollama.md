# 🚀 Day 21 — AI Tool Calling 🛠️🤖

Build a practical AI DevOps Assistant that uses Ollama/Llama 3.2 to select and execute Python tools based on the user's request.

## 🎯 Goal

The AI assistant should:

- Understand the user's request
- Decide whether a tool is required
- Select the appropriate tool
- Generate tool arguments
- Execute the Python function
- Return the tool result to Ollama
- Generate a final natural-language answer
- Support multiple DevOps-oriented tools

## 🏗️ Architecture

User Request → Ollama/Llama 3.2 → Tool Selection → Python Function → Tool Result → Ollama/Llama 3.2 → Final Answer

## 🛠️ Tech Stack

- Python 3.13
- Ollama
- Llama 3.2 3B
- Ollama Python SDK
- Python Functions
- JSON Tool Schemas

## 📁 Project Structure

Day-21/
├── app.py
├── tools.py
├── test_tools.py
├── requirements.txt
└── README.md

## 🔧 Tools

The assistant will have four tools:

### Calculator

    calculate(expression)

Example:

    What is 45 × 27?

Tool call:

    calculate("45 * 27")

Result:

    1215


### Server Status

    get_server_status(server)

Example:

    Check the production server status.

Result:

    Production → HEALTHY


### Disk Usage

    get_disk_usage(server)

Example:

    What is the disk usage on production?

Result:

    Production → 78%


### Service Status

    check_service(server, service)

Example:

    Is nginx running on production?

Result:

    Nginx → RUNNING

## 1. Verify Ollama

Check Ollama:

    ollama --version

Check installed models:

    ollama list

Expected:

    llama3.2:3b

Test the model:

    ollama run llama3.2:3b

Ask:

    Hello

Exit:

    /bye

## 2. Project Environment

Activate the existing virtual environment:

    source venv/Scripts/activate

Verify Python:

    python --version

Expected:

    Python 3.13.14

## 3. requirements.txt

    ollama

Install:

    python -m pip install -r requirements.txt

Verify:

    pip show ollama

## 4. tools.py

    def calculate(expression: str):

        try:

            result = eval(
                expression,
                {"__builtins__": {}},
                {}
            )

            return {
                "expression": expression,
                "result": result
            }

        except Exception as e:

            return {
                "expression": expression,
                "error": str(e)
            }


    def get_server_status(server: str):

        servers = {
            "production": "HEALTHY",
            "test": "WARNING",
            "development": "HEALTHY"
        }

        status = servers.get(
            server.lower(),
            "UNKNOWN"
        )

        return {
            "server": server,
            "status": status
        }


    def get_disk_usage(server: str):

        disk_usage = {
            "production": 78,
            "test": 91,
            "development": 45
        }

        usage = disk_usage.get(
            server.lower()
        )

        if usage is None:

            return {
                "server": server,
                "error": "Server not found"
            }

        return {
            "server": server,
            "disk_usage_percent": usage
        }


    def check_service(server: str, service: str):

        services = {

            "production": {
                "tomcat": "RUNNING",
                "nginx": "RUNNING",
                "oracle": "RUNNING"
            },

            "test": {
                "tomcat": "RUNNING",
                "nginx": "STOPPED",
                "oracle": "RUNNING"
            },

            "development": {
                "tomcat": "RUNNING",
                "nginx": "RUNNING",
                "oracle": "STOPPED"
            }
        }

        server_services = services.get(
            server.lower()
        )

        if server_services is None:

            return {
                "server": server,
                "service": service,
                "error": "Server not found"
            }

        status = server_services.get(
            service.lower(),
            "UNKNOWN"
        )

        return {
            "server": server,
            "service": service,
            "status": status
        }

## 5. test_tools.py

    from tools import (
        calculate,
        get_server_status,
        get_disk_usage,
        check_service
    )


    print("Calculator:")

    print(
        calculate("45 * 27")
    )


    print("\nServer Status:")

    print(
        get_server_status("production")
    )


    print("\nDisk Usage:")

    print(
        get_disk_usage("production")
    )


    print("\nService Status:")

    print(
        check_service(
            "production",
            "nginx"
        )
    )

Run:

    python test_tools.py

Expected:

    Calculator:
    {'expression': '45 * 27', 'result': 1215}

    Server Status:
    {'server': 'production', 'status': 'HEALTHY'}

    Disk Usage:
    {'server': 'production', 'disk_usage_percent': 78}

    Service Status:
    {'server': 'production', 'service': 'nginx', 'status': 'RUNNING'}

## 6. app.py

    import json

    from ollama import chat

    from tools import (
        calculate,
        get_server_status,
        get_disk_usage,
        check_service
    )


    MODEL = "llama3.2:3b"


    tools = [

        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Calculate a mathematical expression.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression such as 45 * 27"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "get_server_status",
                "description": "Get the health status of a server.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "server": {
                            "type": "string",
                            "description": "Server name such as production, test, or development"
                        }
                    },
                    "required": ["server"]
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "get_disk_usage",
                "description": "Get disk usage percentage of a server.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "server": {
                            "type": "string",
                            "description": "Server name"
                        }
                    },
                    "required": ["server"]
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "check_service",
                "description": "Check the status of a service on a server.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "server": {
                            "type": "string",
                            "description": "Server name"
                        },
                        "service": {
                            "type": "string",
                            "description": "Service name such as tomcat, nginx, or oracle"
                        }
                    },
                    "required": [
                        "server",
                        "service"
                    ]
                }
            }
        }
    ]


    available_functions = {

        "calculate": calculate,

        "get_server_status":
            get_server_status,

        "get_disk_usage":
            get_disk_usage,

        "check_service":
            check_service
    }


    messages = [

        {
            "role": "system",
            "content": """
    You are an AI DevOps assistant.

    You have access to tools for:

    - mathematical calculations
    - server status
    - disk usage
    - service status

    Use a tool whenever the user asks for
    information that requires one.

    Do not invent server, disk, or service information.
    """
        }
    ]


    while True:

        question = input("\nYou: ")

        if question.lower() in [
            "exit",
            "quit"
        ]:

            print("Goodbye!")

            break


        messages.append({
            "role": "user",
            "content": question
        })


        response = chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )


        if response.message.tool_calls:

            messages.append(
                response.message
            )


            for tool_call in response.message.tool_calls:

                tool_name = (
                    tool_call.function.name
                )

                arguments = (
                    tool_call.function.arguments
                )


                print(
                    f"\n🔧 Tool: {tool_name}"
                )

                print(
                    f"📥 Arguments: {arguments}"
                )


                function = (
                    available_functions.get(
                        tool_name
                    )
                )


                if function is None:

                    result = {
                        "error":
                        f"Unknown tool: {tool_name}"
                    }

                else:

                    try:

                        result = function(
                            **arguments
                        )

                    except Exception as e:

                        result = {
                            "error": str(e)
                        }


                print(
                    f"📤 Result: {result}"
                )


                messages.append({

                    "role": "tool",

                    "tool_name":
                        tool_name,

                    "content":
                        json.dumps(result)
                })


            final_response = chat(

                model=MODEL,

                messages=messages
            )


            print(
                f"\n🤖 AI: "
                f"{final_response.message.content}"
            )


            messages.append(
                final_response.message
            )


        else:

            print(
                f"\n🤖 AI: "
                f"{response.message.content}"
            )


            messages.append(
                response.message
            )

## 7. Run

Start the application:

    python app.py

The application should display:

    You:

## 🧪 Test 1 — Calculator

Ask:

    What is 45 * 27?

Expected flow:

    User
    ↓
    Ollama
    ↓
    calculate
    ↓
    calculate("45 * 27")
    ↓
    1215
    ↓
    Ollama
    ↓
    Final Answer

Example:

    🔧 Tool: calculate
    📥 Arguments: {'expression': '45 * 27'}
    📤 Result: {'expression': '45 * 27', 'result': 1215}

    🤖 AI: 45 × 27 = 1,215.

## 🧪 Test 2 — Server Status

Ask:

    Check the production server status.

Expected:

    🔧 Tool: get_server_status

    📥 Arguments:
    {'server': 'production'}

    📤 Result:
    {'server': 'production', 'status': 'HEALTHY'}

    🤖 AI: The production server is currently healthy.

## 🧪 Test 3 — Disk Usage

Ask:

    What is the disk usage on production?

Expected:

    🔧 Tool: get_disk_usage

    📥 Arguments:
    {'server': 'production'}

    📤 Result:
    {'server': 'production', 'disk_usage_percent': 78}

    🤖 AI: Production is currently using 78% disk space.

## 🧪 Test 4 — Service Status

Ask:

    Is nginx running on production?

Expected:

    🔧 Tool: check_service

    📥 Arguments:
    {
        'server': 'production',
        'service': 'nginx'
    }

    📤 Result:
    {
        'server': 'production',
        'service': 'nginx',
        'status': 'RUNNING'
    }

    🤖 AI: Nginx is running on the production server.

## 🧪 Test 5 — Different Server

Ask:

    Check nginx on the test server.

Expected:

    nginx → STOPPED

Ask:

    What is the disk usage on test?

Expected:

    test → 91%

## 🧪 Test 6 — Normal Question

Ask:

    What is Docker?

The assistant should answer without calling one of the DevOps tools.

This demonstrates:

    Tool Required?
          ↓
       YES / NO
          ↓
    YES → Execute Tool
    NO  → Normal Answer

## 🔄 Tool Calling Flow

    User Request
          ↓
        Ollama
          ↓
    Tool Selection
          ↓
    Tool Arguments
          ↓
    Python Application
          ↓
    Python Function
          ↓
      Tool Result
          ↓
        Ollama
          ↓
     Final Answer

## 🧠 Important Concept

The LLM does NOT directly execute Python.

The LLM decides:

    Which tool?
    What arguments?

The Python application executes:

    function(**arguments)

Then the result is returned to the LLM.

Example:

    User:
    Check production status.

    ↓

    LLM:
    get_server_status

    ↓

    Arguments:
    {
        "server": "production"
    }

    ↓

    Python:
    get_server_status("production")

    ↓

    Result:
    {
        "server": "production",
        "status": "HEALTHY"
    }

    ↓

    LLM:

    The production server is healthy.

## 🏗️ Final Architecture

                    ┌───────────────┐
                    │     USER      │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    OLLAMA     │
                    │ Llama 3.2 3B  │
                    └───────┬───────┘
                            ↓
                       Tool Selection
                            ↓
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
    Calculator        Server Status       Disk Usage
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ↓
                     Service Status
                            ↓
                    Python Functions
                            ↓
                       Tool Result
                            ↓
                    ┌───────────────┐
                    │    OLLAMA     │
                    └───────┬───────┘
                            ↓
                      Final Answer

## 🆚 Day 20 → Day 21

### Day 20

    User
    ↓
    Search Knowledge
    ↓
    ChromaDB
    ↓
    Context
    ↓
    Ollama
    ↓
    Answer

RAG teaches the AI to **retrieve information**.

### Day 21

    User
    ↓
    Ollama
    ↓
    Select Tool
    ↓
    Python Function
    ↓
    Tool Result
    ↓
    Ollama
    ↓
    Answer

Tool Calling teaches the AI to **use external capabilities**.

## 📌 Key Learning

Day 21 introduces:

- Function calling
- Tool definitions
- Tool descriptions
- JSON schemas
- Tool parameters
- Tool selection
- Argument generation
- Python function execution
- Tool results
- Multiple tools
- Error handling
- LLM + external functions

The important distinction is:

    LLM
    ↓
    Decides what to do

    Python Application
    ↓
    Actually does it

    LLM
    ↓
    Explains the result

## ✅ Completion Checklist

- [ ] Ollama installed
- [ ] Llama 3.2 3B available
- [ ] Virtual environment activated
- [ ] Ollama Python package installed
- [ ] requirements.txt created
- [ ] tools.py created
- [ ] Python tools tested
- [ ] Tool schemas created
- [ ] Tool registry created
- [ ] Ollama tool calling implemented
- [ ] Calculator tested
- [ ] Server status tested
- [ ] Disk usage tested
- [ ] Service status tested
- [ ] Multiple tools working
- [ ] Final LLM response generated

## 🏆 Final Result

A local AI DevOps Tool-Calling Assistant using:

    Python
    +
    Ollama
    +
    Llama 3.2 3B
    +
    Custom Python Tools

The assistant can understand a request, select the correct tool, pass arguments to Python, execute the function, receive the result, and generate a natural-language response.