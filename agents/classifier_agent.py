from pathlib import Path
from chain.agent_chain import classifier_agent_chain
from langchain_community.document_loaders import PyPDFLoader

class ClassifierAgent():

    def classify(self, filename):

        UPLOAD_DIR = Path(__file__).resolve().parents[1] / "local_uploads"
        file_path = UPLOAD_DIR / filename

        if "pdf" in filename:
            loader = PyPDFLoader(file_path)
            pages = []
            for page in loader.lazy_load():
                pages.append(page)
            content = pages[0].page_content
            print(content)

        else:
            with open(file_path, 'rb') as file:
                content = file.read().decode("utf-8", errors="ignore")
                print(content)

        return classifier_agent_chain.invoke({'input': content}), content
