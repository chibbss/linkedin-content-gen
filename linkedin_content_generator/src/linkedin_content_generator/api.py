from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import json

from crew import LinkedinContentGenerator

# FastAPI app setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start time for health check
start_time = datetime.utcnow()

# Crew instance
crew_instance = LinkedinContentGenerator()

# Input model
class CrewInput(BaseModel):
    topic: str
    brand_voice: Optional[str] = None
    cta_link: Optional[str] = None
    mission: Optional[str] = None
    product: Optional[str] = None
    company_name: Optional[str] = None
    viral_post: Optional[dict] = None  # You can make this stricter later with its own model

@app.post("/generate-final-post")
async def generate_final_post(payload: CrewInput):
    try:
        # Log incoming data for debugging
        print("Received input:", payload)

        # Run the crew pipeline
        raw_output = crew_instance.crew().kickoff(inputs=payload.dict())

        # Attempt to serialize the output
        if hasattr(raw_output, "dict"):
            raw_output = raw_output.dict()
        elif hasattr(raw_output, "to_dict"):
            raw_output = raw_output.to_dict()

        # Handle structured JSON output
        if isinstance(raw_output, dict):
            if 'json_dict' in raw_output:
                return JSONResponse(content=raw_output['json_dict'], status_code=200)
            elif 'raw' in raw_output:
                try:
                    parsed = json.loads(raw_output['raw'])
                    return JSONResponse(content=parsed, status_code=200)
                except json.JSONDecodeError:
                    return JSONResponse(content=raw_output, status_code=200)

        # Fallback return
        return JSONResponse(content=raw_output, status_code=200)

    except Exception as e:
        print(f"Error in /generate-final-post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", tags=["Health Check"])
def health_check():
    uptime: timedelta = datetime.utcnow() - start_time
    return JSONResponse(
        content={
            "status": "ok",
            "uptime": str(uptime)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)