from pathlib import Path
from typing import Any
from fastapi import APIRouter, File, UploadFile
from agents.classifier_agent import ClassifierAgent
from agents.email_agent import EmailAgent
import json
import logging
import httpx
from agents.json_agent import JsonAgent
import shutil
from agents.pdf_agent import PdfAgent
from chain.email_agent_final_response_chain import email_agent_final_response_chain
import chardet

# Configure the logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Conifgure logging in file
file_handler = logging.FileHandler('classifier.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Configure logging in console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) 
console_handler.setFormatter(formatter)

# Add both the file and console log handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def read_log_file():

    UPLOAD_DIR = Path(__file__).resolve().parents[3]
    file_path = UPLOAD_DIR / "classifier.log"

    # Detect encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    
    # Read with detected encoding
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        content = f.read()
    
    with open(file_path, 'w') as f:
        pass

    return content

router = APIRouter()

@router.get("/")
def home():
    return {"message": "scrapper_service"}

# Main /crm route
@router.post("/crm")
async def escalate(file: UploadFile = File(...)):

    UPLOAD_DIR = Path(__file__).resolve().parents[3] / "local_uploads"

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info("Classifying the input content...")

    # Instantiate Classifier Agent Object
    classifier_agent = ClassifierAgent()

    # Classify content
    classified_result, content = classifier_agent.classify(file.filename)

    logger.info(f"Content classified successfully with info: {classified_result.content}")

    # Convert the classified content to python dictionary
    classified_result = json.loads(classified_result.content)


    logger.info(f"Format: {classified_result['Final Answer']['format']}")
    logger.info(f"Intent: {classified_result['Final Answer']['intent']}")
    
    # Check if the content is of format email
    if classified_result['Final Answer']["format"] == "email":

        logger.info("Take action control to email agent...")

        # If the content type is email then create an Emain Agent
        email_agent = EmailAgent()

        # Analyze the contents of email
        analyzed_email_result = email_agent.analyze(content)
        logger.info("Analyzed email content")

        # Conver the analyzed content to python dictionary
        print(f"analyzed_email_result: {analyzed_email_result}")
        analyzed_email_result = json.loads(analyzed_email_result)

        # If the issue type in the email is complaint and urgency is high and tone is anger     
        if analyzed_email_result['urgency'] == 'high' and (analyzed_email_result['tone'] == 'anger' or analyzed_email_result['tone'] == 'escalation'):

            logger.warning("The urgency of the email is high and tone is angry")
            logger.info("Routing the call to : POST /crm/escalate")

            async with httpx.AsyncClient() as client:

                # Route the action to POST /crm/escalate
                result = await client.post("http://localhost:8000/api/v1/crm/escalate",
                    json={'email': classified_result['Question'], 'urgency': analyzed_email_result['urgency'], 'tone': analyzed_email_result['tone'], 'intent': classified_result['Final Answer']['intent']},
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
    # Else check if the format is json
    elif classified_result['Final Answer']['format'] == "json":

        try:
            logger.info("Take action to json agent...")

            # Instantiating json agent
            json_agent = JsonAgent()

            logger.info("Loading json content")
            # Loading json data from the recieved file
            json_data = json.loads(content)
            logger.info("Loaded json content")
            
            logger.info("Validating json data...")
            # Check if the json validates with the pre-defined schema
            if json_agent.validate_json_schema(json_data):

                logger.info("Json data is valid")
                logger.info("\n")

                with open('classifier.log', 'rb') as file:
                    content = file.read()

                # Return positive message is the json is valid
                return {"message": "the json is valid", "logs": content}
        
        
        except:
            # If the json is not valid then route the api call to : POST /rist_alert
            async with httpx.AsyncClient() as client:

                logger.info("Json data is not valid")
                logger.info("Calling action route: POST /risk_alert")

                # Route the action to POST /risk_alert
                result = await client.post("http://localhost:8000/api/v1/risk_alert",
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
    # Finally the content is in pdf format
    else:
        # Instantiate pdf agent
        pdf_agent = PdfAgent()
        result = pdf_agent.analyze_pdf(content)

        logger.info("\n")

        log_content = read_log_file()
        
        # Return the json converted pdf content
        return {"message": result, "logs": log_content}

    log_content = read_log_file()

    return {"message": result.json()["final_response"], "logs": log_content}

# /crm/escalate route
@router.post("/crm/escalate")
def escalate(data: dict[str, Any]):
    logger.info("Control is inside the route: POST /crm/escalate")
    logger.info("\n")
    final_email_response = email_agent_final_response_chain.invoke(data)
    return {"final_response": final_email_response}

# /rist_alert route
@router.post("/risk_alert")
def risk_alert():
    logger.info("Control is inside the route: POST /rist_alert")
    logger.info("\n")
    return {"final_response": "the provided json data is invalid and risk alert recieved"}

@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}