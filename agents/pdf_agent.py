from chain.pdf_agent_chain import pdf_agent_chain

class PdfAgent():
    
    def analyze_pdf(self, content):
        return pdf_agent_chain.invoke({"content": content})