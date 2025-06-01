from langchain_core.prompts import ChatPromptTemplate

email_agent_prompt_template = ChatPromptTemplate(
    [
        ('system', 
            """
                You are a helpful email analyzer

                You will be give the email body as input and you have to extract structured fields like sender, urgency, issue/request and tone(escalation, polite, threatening).

                After extracting all the fields you have to return the response in json format only and not in markdown, just simple json like shown below:

                {{
                    "sender": "sender which you extracted",
                    "urgency": "high or low",
                    "email_type": "issue or request",
                    "tone": "tone of email"
                }}
            """ 
        ),
        ('user', 'email: {email}')
    ]
)