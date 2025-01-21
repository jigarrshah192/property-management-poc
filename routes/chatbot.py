from fastapi import APIRouter, Form
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from fastapi.responses import JSONResponse
from config import OPENAI_API_KEY
from constants import LLM_MODEL, TEMPERATURE
import logging
from utils.common import error_response, success_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def initialize_memory():
    return ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key="answer"
    )


@router.post("/query")
async def query_chatbot(session_id: str = Form(...), question: str = Form(...)):
    persist_directory = f"./chroma_store/{session_id}"
    memory = initialize_memory()

    try:
        vectorstore = Chroma(
            collection_name=f"session_{session_id}",
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings(api_key=OPENAI_API_KEY),
        )
    except Exception as e:
        logger.error(f"Failed to load session {session_id}: {e}")
        return error_response(f"Failed to load session: {e}", error_code=500)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            temperature=TEMPERATURE, model=LLM_MODEL, api_key=OPENAI_API_KEY
        ),
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
    )

    try:
        response = qa_chain(
            {"question": question, "chat_history": memory.chat_memory.messages}
        )
        memory.chat_memory.add_user_message(question)
        memory.chat_memory.add_ai_message(response["answer"])
    except Exception as e:
        logger.error(f"Error during QA chain execution for session {session_id}: {e}")
        return error_response(f"Failed to process query: {e}", error_code=500)

    return success_response(
        data={"answer": response.get("answer", "No answer available")}
    )
