# Chat Assistant

This project provides a Chat Assistant with a web-based frontend and a backend powered by FastAPI. The application allows users to upload documents, interact with a chatbot for property-related queries, and manage sessions effectively.

## Features
- Upload multiple document types (PDF, DOCX, CSV, XLSX).
- Query a chatbot based on uploaded documents.
- Reset sessions to clear data.

---

## Prerequisites
Make sure you have the following installed:
- Python 3.8+
- FastAPI
- Uvicorn

### Install Required Libraries
Install the dependencies using `pip`:
```bash
pip install -r requirements.txt
```

---

## Running the Application

### 1. Frontend
To serve the frontend, use Python's built-in HTTP server:
```bash
cd frontend
python -m http.server 8080
```
Access the frontend in your browser at:
```
http://127.0.0.1:8080/frontend/index.html
```

### 2. Backend
Run the FastAPI backend using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The backend will be available at:
```
http://127.0.0.1:8000
```

---

## API Endpoints

### Upload Documents
**POST** `/documents/upload`
- **Body**: Multipart form data with file uploads.
- **Response**: Session ID and upload status.

### Query Chatbot
**POST** `/chat/query`
- **Form Data**:
  - `session_id`: ID of the active session.
  - `question`: User's query.
- **Response**: Chatbot's answer.

### Reset Session
**POST** `/session/reset`
- **Form Data**:
  - `session_id`: ID of the session to reset.
- **Response**: Status of session reset.

---

## Notes
- Ensure the backend is running before using the frontend.
- Uploaded files are stored temporarily in the backend during the session.

---

## Contributing
Feel free to submit issues or pull requests for improvements and new features.



