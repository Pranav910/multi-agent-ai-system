from chain.email_agent_chain import email_agent_chain

class EmailAgent():

    def analyze(self, _email):
        return email_agent_chain.invoke({'email': _email})
