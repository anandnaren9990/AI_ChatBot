import httpx
import resources.llm_properties as llm_pr
from app_log import logger
import time

async def llm_response(model, messages):
    logger.info("Sending input to LLM...")
    payload = {
        "model" : model,
        "messages" : messages,
        "stream" : False
    }
    
    try: 
        start = time.time()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url=llm_pr.llm_chat_url, json=payload)
            response.raise_for_status()
            data = response.json()
            llm_output = data["message"]["content"]
            if not llm_output and data.get("done_reason") == "load":
                logger.info("Model was loaded by Ollama. Retrying chat request...")
                response = await client.post(url=llm_pr.llm_chat_url, json=payload)
                response.raise_for_status()
                data = response.json()
                logger.info(f"llm_output_retry: {data}")
                llm_output = data["message"]["content"]
            duration = time.time() - start
            logger.info(f"LLM response time: {duration:.2f}s")
            return llm_output
    except httpx.ConnectError as e:
        logger.error(f"Error - Could not connect to LLM: {e}")
        raise
    except httpx.ConnectTimeout as e:
        logger.error(f"LLM took long time to respond: {e}")
        raise
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occured: {e}")
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
