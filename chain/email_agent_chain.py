from prompts.email_agent_prompt import email_agent_prompt_template
from models.classifier_model import llm
from langchain_core.output_parsers import StrOutputParser

email_agent_chain = email_agent_prompt_template | llm | StrOutputParser()