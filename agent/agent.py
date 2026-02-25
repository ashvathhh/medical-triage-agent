from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from agent.tools import search_pubmed, check_drug_info, assess_urgency
import os

load_dotenv()

def create_medical_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=1024
    )

    tools = [search_pubmed, check_drug_info, assess_urgency]

    system_prompt = """You are a medical triage assistant. For every patient case:
1. Always call assess_urgency first
2. Call search_pubmed once with a short 2-3 word query
3. Only call check_drug_info if a specific drug is mentioned
4. Give a concise structured response under 200 words
Do not repeat tool calls. Be fast and concise."""

    agent = create_react_agent(
        llm,
        tools,
        prompt=system_prompt
    )

    return agent