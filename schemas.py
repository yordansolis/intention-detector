from pydantic import BaseModel
from typing import List, Dict

class Message(BaseModel):
    text: str
    intentions: List[str]

class IntentionResponse(BaseModel):
    detected_intention: str
    confidence: float
    explanation: str
    action: Dict


