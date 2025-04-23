"""
Simple example of using FastAPI-MCP to add an MCP server to a FastAPI app.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from azure.communication.email import EmailClient
import requests, uuid, json, os
from dotenv import find_dotenv, load_dotenv


app = FastAPI()
load_dotenv(find_dotenv())

# Greet Tool
class GreetRequest(BaseModel):
    name: str

@app.post("/greet", operation_id="greet_user_by_name")
async def greet(request: GreetRequest):
    """Greet the user with a personalized message."""
    return JSONResponse(content={"message": f"Hellooo {request.name}"})


# Email Tool
class EmailRequest(BaseModel):
    to: str
    subject: str
    text: str
    html: str = None  # Optional HTML version of the email

@app.post("/send-email", operation_id="send_email")
async def send_email(request: EmailRequest):
    """Send an email using Azure Communication Services."""
    try:
        connection_string = "null"  # Replace with your valid connection string
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@f4f19d5b-a3a2-4007-b3dc-4668d8eccd3a.azurecomm.net",
            "recipients": {
                "to": [{"address": request.to}]
            },
            "content": {
                "subject": request.subject,
                "plainText": request.text,
                "html": request.html or f"<html><body><p>{request.text}</p></body></html>"
            },
        }

        poller = client.begin_send(message)
        result = poller.result()

        return JSONResponse(content={"message": "Email sent successfully", "message_id": result.message_id})
    except Exception as ex:
        return JSONResponse(status_code=500, content={"error": str(ex)})
    
# Translator Tool
# Replace with your actual credentials
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
TRANSLATOR_REGION = "eastus"

print(TRANSLATOR_KEY)

class TranslateRequest(BaseModel):
    text: str
    from_lang: str = "ja"           # Default: Japanese
    to_langs: str = "en" 

@app.post("/translate-text", operation_id="translate_text")
async def translate_text(request: TranslateRequest):
    """Translate text using Microsoft Translator API."""
    try:
        path = '/translate'
        constructed_url = TRANSLATOR_ENDPOINT + path

        params = {
            'api-version': '3.0',
            'from': request.from_lang,
            'to': request.to_langs.split(",")
        }

        headers = {
            'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
            'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': request.text}]
        api_response = requests.post(constructed_url, params=params, headers=headers, json=body)
        result = api_response.json()

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    #example status: FastAPI との MCP 統合が完了しました。
    #example status 2: もう終わりです