from langchain_core.prompts import ChatPromptTemplate

pdf_agent_prompt = ChatPromptTemplate(
    [
        ('system', """
                        You are helpful pdf content analyzer. You will given the content of the pdf and you have to make a json summary of all that content. Return the response only in json format without any explanation just simple json.
        """),
        ('user', "content: {content}")
    ]
)