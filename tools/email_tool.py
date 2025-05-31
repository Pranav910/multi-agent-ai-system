from langchain.tools import tool

@tool
def call_email_tool(email: str):
    """this is the tool to analyze email"""
    from ..agents.email_agent import EmailAgent
    return EmailAgent.analyze(email)
