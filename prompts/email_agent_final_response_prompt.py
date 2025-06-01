from langchain_core.prompts import ChatPromptTemplate

email_agent_final_response_prompt = ChatPromptTemplate(
    [
        ('system', """

            You are a helpful summarizer assistant. 
         
            ---
         
            You will be give the email: {email} 
         
            and the attributes of the email like 
         
            content: {email}, 
            tone: {tone}, 
            urgency: {urgency} and 
            intent: {intent}.

            ---

            You have to summarize the given email and its attributes and generate the response in proper markdown.
        """)
    ]
)