from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain import hub
from dotenv import load_dotenv
from agent.tools import search_pubmed, check_drug_info, assess_urgency
import os

load_dotenv()

def create_medical_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    tools = [search_pubmed, check_drug_info, assess_urgency]

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    prompt = hub.pull("hwchase17/react-chat")

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor