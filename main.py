from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import document_management, chatbot, session_management
from config import CORS_ALLOWED_ORIGINS,APP_HOST,APP_PORT

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(document_management.router, prefix="/documents", tags=["Document Management"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(session_management.router, prefix="/session", tags=["Session Management"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)