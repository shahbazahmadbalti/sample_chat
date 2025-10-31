from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import openai
import os
import uvicorn
from typing import List, Dict

app = FastAPI(title="Sample Chatbot", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: str

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

openai.api_key = OPENAI_API_KEY

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Frontend files not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Chatbot is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatMessage):
    """Handle chat requests"""
    try:
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful, friendly AI assistant. Keep responses concise and informative."}
        ]
        
        # Add conversation history
        messages.extend(chat_request.history)
        
        # Add current message
        messages.append({"role": "user", "content": chat_request.message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract response
        assistant_message = response.choices[0].message.content
        
        return ChatResponse(
            response=assistant_message,
            timestamp="2025-10-31T05:40:49Z"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/api/models")
async def get_available_models():
    """Get available OpenAI models"""
    try:
        models = openai.Model.list()
        available_models = [model.id for model in models.data if "gpt" in model.id]
        return {"models": available_models}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
