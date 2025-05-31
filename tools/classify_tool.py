from langchain.tools import tool

@tool
def classifiy_content(content: str):
    """this is the tool for classifying the content based on email, json and pdf"""
    