from langchain_core.prompts import ChatPromptTemplate

pdf_agent_final_response_prompt = ChatPromptTemplate(

    [
        ('system', """

            You are a helpful pdf content summarizer agent.

            You will be given the content: {content} of the pdf and you have to summarize that content.
         
            Generate the final response in markdown.
        """)
    ]
)