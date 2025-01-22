class ChatbotUI {
    constructor() {
        this.initialize();
        this.bindEvents();
    }

    initialize() {
        // DOM elements
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendMessage');
        this.roleSelect = document.getElementById('userRole');
        this.uploadButton = document.getElementById('uploadButton');
        this.fileUploadArea = document.getElementById('fileUploadArea');
        this.pdfFileInput = document.getElementById('pdfFile');
        this.cancelUpload = document.getElementById('cancelUpload');

        // State
        this.isProcessing = false;
    }

    bindEvents() {
        // Message sending
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // File upload handling
        this.uploadButton.addEventListener('click', () => this.toggleFileUpload());
        this.cancelUpload.addEventListener('click', () => this.toggleFileUpload());
        this.pdfFileInput.addEventListener('change', (e) => this.handleFileUpload(e));

        // Auto-resize textarea
        this.userInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    async sendMessage() {
        if (this.isProcessing || !this.userInput.value.trim()) return;

        const message = this.userInput.value.trim();
        const role = this.roleSelect.value;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        this.userInput.value = '';
        this.autoResizeTextarea();

        // Show processing state
        this.isProcessing = true;
        this.sendButton.disabled = true;

        try {
            const response = await this.sendMessageToBackend(message, role);
            this.addMessageToChat(response.response, 'bot');
        } catch (error) {
            this.addMessageToChat('Sorry, there was an error processing your request.', 'bot');
        } finally {
            this.isProcessing = false;
            this.sendButton.disabled = false;
        }
    }

    async sendMessageToBackend(message, role) {
        const response = await fetch('/chatbot/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify({ query: message, role: role }),
        });

        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/chatbot/api/summarize/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: formData,
            });

            const data = await response.json();
            if (data.summary) {
                this.addMessageToChat(`Summary of ${file.name}:`, 'bot');
                this.addMessageToChat(data.summary, 'bot');
            } else {
                this.addMessageToChat('Sorry, I could not process the PDF file.', 'bot');
            }
        } catch (error) {
            this.addMessageToChat('Error processing the PDF file.', 'bot');
        } finally {
            this.toggleFileUpload();
            this.pdfFileInput.value = '';
        }
    }

    addMessageToChat(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = message;
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    toggleFileUpload() {
        const isVisible = this.fileUploadArea.style.display === 'block';
        this.fileUploadArea.style.display = isVisible ? 'none' : 'block';
    }

    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = `${this.userInput.scrollHeight}px`;
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotUI();
});
