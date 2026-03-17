from fastapi import APIRouter

from src.genAI.controller import *
from src.genAI.dtos import *


genairouter=APIRouter()

@genairouter.post("/ai_chat")
def gen_ai(body:genAISchema):
    return generate_ai_chat(body)