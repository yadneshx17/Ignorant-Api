import subprocess
import json
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production (e.g., ["https://yourfrontend.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# API Key Setup
API_KEY = os.getenv("API_KEY", "default-api-key")  # Fallback in case .env is missin
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Function to check API key
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/ignorant/{country_code}/{phone_number}")
def run_ignorant(country_code: str, phone_number: str, api_key: str = Depends(get_api_key)):
    try:
        # Runs IGNORANT tool
        result = subprocess.run(
            ["ignorant", country_code, phone_number],  
            capture_output=True, text=True
        )

        output = result.stdout.strip()
        return {"country_code": country_code, "phone_number": phone_number, "data": output}
    
    except Exception as e:
        return {"error": str(e)}


# API without authentication.
"""
@app.get("/ignorant/{country_code}/{phone_number}")
def run_ignorant(country_code: str, phone_number: str):
    try:
        result = subprocess.run(
            ["ignorant", country_code, phone_number],  
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        return {"country_code": country_code, "phone_number": phone_number, "data": output}
    
    except Exception as e:
        return {"error": str(e)}
"""
