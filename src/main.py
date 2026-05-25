import uvicorn
import app
from app_log import logger

if __name__ == "__main__":
    logger.info("Starting FastApi Server...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )