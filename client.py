from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    })
    
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()
    print(tools)
    model = ChatGroq(model="moonshotai/kimi-k2-instruct-0905")
    agent = create_react_agent(model, tools)
    
    print("Ask me anything! Type 'quit' to exit.")
    print(tools)
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        print("Bot:", response['messages'][-1].content)

asyncio.run(main())
