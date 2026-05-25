from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app_log import logger
from resources.resources import prompt
from services.llm_service import llm_response
from resources.llm_properties import model

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

conversation_history = []

@app.post("/llmchat")
async def chat_with_llm(request: ChatRequest):
    logger.info("Starting the chat with LLM...")
    try: 
        conversation_history.append(
            {
                "role" : "user",
                "content" : request.user_input
            }
        )
        messages = conversation_history[-10:]
        llm_output = await llm_response(model=model, messages=messages)
        conversation_history.append(
            {
                "role" : "assistant",
                "content" : llm_output
            }    
        )
        return {"response": llm_output}
    except Exception as e:
        logger.error(f"Error occured: {e}")
        raise HTTPException(status_code=500, detail="Failed to get LLM response")
