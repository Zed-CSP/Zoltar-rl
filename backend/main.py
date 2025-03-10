from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import joblib
from pathlib import Path
from rl_model import AkinatorRL
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class PredictionRequest(BaseModel):
    answers: Dict[str, int]

class PredictionResponse(BaseModel):
    prediction: Optional[str] = None
    next_question: Optional[str] = None
    confidence: Optional[float] = None

class FeedbackRequest(BaseModel):
    entity: str
    correct: bool
    answers: Dict[str, int]

# Initialize the RL model
rl_model = AkinatorRL()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    answers = request.answers
    
    logger.info(f"Received answers: {answers}")
    
    # Get prediction based on current answers
    prediction, confidence = rl_model.predict(answers)
    
    if prediction:
        logger.info(f"Made prediction: {prediction} with confidence {confidence}")
        return {"prediction": prediction, "confidence": confidence}
    
    # If no confident prediction, get the next question
    next_question = rl_model.get_next_question(answers)
    
    if not next_question:
        logger.warning("No next question available")
        return {"prediction": "I don't know what you're thinking of!", "confidence": 0.0}
    
    logger.info(f"Next question: {next_question}")
    return {"next_question": next_question, "confidence": confidence}

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    """
    Endpoint to receive feedback on predictions to improve the model
    """
    rl_model.update_from_feedback(
        entity=request.entity,
        answers=request.answers,
        correct=request.correct
    )
    
    return {"status": "Feedback received and model updated"}

@app.post("/add-question")
async def add_question(question: str):
    """Add a new question to the system"""
    rl_model.add_question(question)
    return {"status": "Question added"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get("/admin/data")
async def get_admin_data():
    """Get all questions and entities for the admin interface"""
    return {
        "questions": rl_model.questions,
        "entities": rl_model.entities
    }

@app.get("/debug")
async def debug():
    """Get debug information about the current state of the system"""
    return {
        "num_questions": len(rl_model.questions),
        "num_entities": len(rl_model.entities),
        "sample_entities": list(rl_model.entities.keys())[:5],
        "sample_questions": rl_model.questions[:5],
        "prediction_threshold": {
            "min_questions": 8,
            "min_confidence": 0.8
        }
    }