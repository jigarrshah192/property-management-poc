from fastapi import APIRouter, UploadFile, File
import os
import uuid
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document as LangchainDocument
from utils.file_processing import process_docx, process_csv, process_xlsx
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from fastapi.responses import JSONResponse
from config import OPENAI_API_KEY
from utils.common import error_response, success_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    session_id = str(uuid.uuid4())
    persist_directory = f"./chroma_store/{session_id}"
    os.makedirs(persist_directory, exist_ok=True)

    documents = []
    for file in files:
        file_path = os.path.join(persist_directory, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        try:
            if file.filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                for doc in docs:
                    documents.append(
                        LangchainDocument(
                            page_content=doc.page_content, metadata=doc.metadata
                        )
                    )
            elif file.filename.endswith(".docx"):
                text = process_docx(file_path)
                documents.append(
                    LangchainDocument(
                        page_content=text, metadata={"source": file.filename}
                    )
                )
            elif file.filename.endswith(".csv"):
                text = process_csv(file_path)
                documents.append(
                    LangchainDocument(
                        page_content=text, metadata={"source": file.filename}
                    )
                )
            elif file.filename.endswith(".xlsx"):
                text = process_xlsx(file_path)
                documents.append(
                    LangchainDocument(
                        page_content=text, metadata={"source": file.filename}
                    )
                )
            else:
                logger.error(f"Unsupported file type: {file.filename}")
                return error_response(
                    f"Unsupported file type: {file.filename}", error_code=400
                )
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            return error_response(
                f"Error processing file {file.filename}: {e}", error_code=500
            )

    try:
        vectorstore = Chroma.from_documents(
            documents,
            OpenAIEmbeddings(api_key=OPENAI_API_KEY),
            collection_name=f"session_{session_id}",
            persist_directory=persist_directory,
        )
        vectorstore.persist()
    except Exception as e:
        logger.error(f"Error creating vectorstore for session {session_id}: {e}")
        return error_response(f"Error creating vectorstore: {e}", error_code=500)

    logger.info(
        f"Uploaded and persisted {len(documents)} documents for session {session_id}."
    )
    return success_response(
        data={"session_id": session_id},
        message=f"Uploaded and persisted {len(documents)} documents.",
    )
