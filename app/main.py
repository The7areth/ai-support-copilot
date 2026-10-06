from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from app.core import Copilot

app = FastAPI(title="AI Support Copilot", version="1.0.0")
copilot = Copilot()
class Ticket(BaseModel):
    text: str = Field(min_length=5, max_length=4000)
    generate: bool = False
    @field_validator("text")
    @classmethod
    def meaningful(cls, value):
        if len(value.strip()) < 5:
            raise ValueError("Provide a meaningful ticket")
        return value.strip()

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).with_name("index.html"))

@app.get("/health")
def health():
    return {"status":"ok", "runbooks":len(copilot.docs)}

@app.post("/api/analyze")
def analyze(ticket: Ticket):
    return copilot.analyze(ticket.text, ticket.generate)
