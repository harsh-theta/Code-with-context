from mcp_use import MCPClient, MCPAgent
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()


if "messages" not in st.session_state:
    st.session_state.messages = []

config = "mcp.json"
client = MCPClient.from_config_file(config)
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv("GEMINI_API_KEY"))



async def generate_response(message):
    try:
        agent = MCPAgent(llm=llm,client=client)
        response = await agent.run(message)
        return response
    except Exception as e:
        st.error(f"Error generating the response: {str(e)}")
        return None

st.title("Code with Context")
st.subheader("Backed by Context7 MCP server")



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(generate_response(prompt))
            if response:
                st.write(response)
