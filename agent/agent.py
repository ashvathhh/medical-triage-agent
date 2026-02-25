from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
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

    agent = create_react_agent(llm, tools)

    return agent