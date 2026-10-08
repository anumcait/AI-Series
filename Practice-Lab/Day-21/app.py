from ollama import chat

from tools import (
    calculate,
    get_server_status,
    get_disk_usage,
    check_service
)


MODEL = "llama3.2:3b"


# ============================================================
# TOOL DEFINITIONS
# ============================================================

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
            "description": "Check whether a service is running on a server.",
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


# ============================================================
# TOOL REGISTRY
# ============================================================

available_functions = {

    "calculate": calculate,

    "get_server_status": get_server_status,

    "get_disk_usage": get_disk_usage,

    "check_service": check_service
}


# ============================================================
# CONVERSATION
# ============================================================

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
actual server or calculation information.

Do not invent infrastructure information.
"""
    }
]


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break


    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })


    # ========================================================
    # ASK OLLAMA
    # ========================================================

    response = chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )


    # ========================================================
    # TOOL CALL?
    # ========================================================

    if response.message.tool_calls:

        # Add assistant tool-call message
        messages.append(response.message)


        # There can be multiple tool calls
        for tool_call in response.message.tool_calls:

            tool_name = tool_call.function.name

            tool_arguments = (
                tool_call.function.arguments
            )


            print(
                f"\n🔧 Tool Selected: {tool_name}"
            )

            print(
                f"📥 Arguments: {tool_arguments}"
            )


            # =================================================
            # FIND PYTHON FUNCTION
            # =================================================

            function = available_functions.get(
                tool_name
            )


            if function is None:

                tool_result = {
                    "error":
                    f"Unknown tool: {tool_name}"
                }

            else:

                try:

                    # =========================================
                    # EXECUTE PYTHON FUNCTION
                    # =========================================

                    tool_result = function(
                        **tool_arguments
                    )

                except Exception as e:

                    tool_result = {
                        "error": str(e)
                    }


            print(
                f"📤 Tool Result: {tool_result}"
            )


            # =================================================
            # SEND RESULT BACK TO LLM
            # =================================================

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": str(tool_result)
            })


        # ====================================================
        # ASK LLM FOR FINAL RESPONSE
        # ====================================================

        final_response = chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )


        print(
            f"\n🤖 AI: {final_response.message.content}"
        )


        messages.append(
            final_response.message
        )


    else:

        # ====================================================
        # NO TOOL REQUIRED
        # ====================================================

        print(
            f"\n🤖 AI: {response.message.content}"
        )

        messages.append(
            response.message
        )