from prompts.pdf_agent_prompt import pdf_agent_prompt
from models.classifier_model import llm
from langchain_core.output_parsers import StrOutputParser

pdf_agent_chain = pdf_agent_prompt | llm | StrOutputParser()