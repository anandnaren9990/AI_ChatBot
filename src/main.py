import uvicorn
import app
from app_log import logger

if __name__ == "__main__":
    logger.info("Starting FastApi Server...")
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )