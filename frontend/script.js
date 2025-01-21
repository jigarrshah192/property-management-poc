const backendBaseURL = "http://127.0.0.1:8000";
let sessionId = null;

const chatSection = document.getElementById('chatSection');
const chatLog = document.getElementById('chatLog');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const resetButton = document.getElementById('resetButton');
const uploadButtonText = document.getElementById('uploadButtonText');
const uploadLoader = document.getElementById('uploadLoader');
const uploadedFiles = document.getElementById('uploadedFiles');

const showUploadedFiles = (files) => {
    uploadedFiles.innerHTML = '';
    if (files.length > 0) {
        uploadedFiles.classList.remove("d-none");
        Array.from(files).forEach(file => {
            const li = document.createElement('li');
            li.textContent = file.name;
            uploadedFiles.appendChild(li);
        });
    } else {
        uploadedFiles.classList.add("d-none");
    }
};

const appendMessage = (text, sender) => {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = sender === 'user' ? 'U' : 'AI';
    const span = document.createElement('span');
    span.textContent = text;
    if (sender === 'user') {
        messageDiv.appendChild(span);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(span);
    }
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
};

toastr.options = {
    closeButton: true,
    progressBar: true,
    timeOut: 3000,
    positionClass: "toast-top-right",
};

document.getElementById('files').addEventListener('change', (e) => {
    showUploadedFiles(e.target.files);
});

uploadForm.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(uploadForm);
    uploadButtonText.classList.add('d-none');
    uploadLoader.classList.remove('d-none');
    try {
        const response = await fetch(`${backendBaseURL}/documents/upload`, { method: 'POST', body: formData });
        const result = await response.json();
        if (result.success) {
            sessionId = result.data.session_id;
            toastr.success(result.message);
            chatSection.style.display = 'block';
            userInput.disabled = false;
            sendButton.disabled = false;
            resetButton.disabled = false;
        } else {
            toastr.error(result.message);
        }
    } catch (error) {
        toastr.error("Error uploading files. Please try again.");
    } finally {
        uploadButtonText.classList.remove('d-none');
        uploadLoader.classList.add('d-none');
    }
};

sendButton.onclick = async () => {
    const question = userInput.value.trim();
    if (!question) return;

    sendButton.disabled = true;
    buttonText.classList.add('d-none');
    buttonLoader.classList.remove('d-none');

    appendMessage(question, 'user');
    userInput.value = '';
    try {
        const formData = new FormData();
        formData.append('session_id', sessionId);
        formData.append('question', question);
        const response = await fetch(`${backendBaseURL}/chatbot/query`, { method: 'POST', body: formData });
        const result = await response.json();
        console.log(result)
        if (result.success) {
            appendMessage(result.data.answer || 'No response available.', 'bot');
        } else {
            appendMessage(result.message, 'bot');
        }
    } catch (error) {
        appendMessage('Error: Unable to fetch response.', 'bot');
    } finally {
        sendButton.disabled = false;
        buttonText.classList.remove('d-none');
        buttonLoader.classList.add('d-none');
    }
};

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendButton.click();
    }
});

resetButton.onclick = async () => {
    if (!sessionId) {
        toastr.error("No active session to reset.");
        return;
    }
    try {
        const response = await fetch(`${backendBaseURL}/session/reset`, {
            method: "POST",
            body: new URLSearchParams({ session_id: sessionId }),
        });
        const result = await response.json();
        if (result.success) {
            toastr.success(result.message);

            // Clear chat log
            chatLog.innerHTML = '';

            // Keep input and send button active for continued chatting
            userInput.value = '';
            userInput.disabled = false;
            sendButton.disabled = false;

            // Retain session ID to allow continued chatting
        } else {
            toastr.error(result.message);
        }
    } catch (error) {
        toastr.error("Error resetting the session. Please try again.");
    }
};

