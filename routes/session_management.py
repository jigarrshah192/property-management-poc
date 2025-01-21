from fastapi import APIRouter, Form
import os
import logging
from utils.common import error_response, success_response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/reset")
async def reset_session(session_id: str = Form(...)):
    persist_directory = f"./chroma_store/{session_id}"

    try:
        if os.path.exists(persist_directory):
            for root, dirs, files in os.walk(persist_directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(persist_directory)
            logger.info(f"Session '{session_id}' has been successfully reset.")
            return success_response(message=f"Session '{session_id}' has been reset.")
        else:
            logger.warning(f"No session found for ID '{session_id}'.")
            return error_response(
                f"No session found for ID '{session_id}'.", error_code=404
            )
    except Exception as e:
        logger.error(f"Failed to reset session '{session_id}': {e}")
        return error_response(f"Failed to reset session: {e}", error_code=500)
