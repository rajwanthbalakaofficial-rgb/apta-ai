/* ==========================================================================
   apta AI - Interactive Application Engine JavaScript
   ========================================================================== */

let currentMode = "universal";
const API_BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
});

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE_URL}/`);
        const data = await res.json();
        const statusElem = document.getElementById("api-status-text");
        if (data.status === "online") {
            statusElem.innerText = data.gemini_status === "configured" ? "Online (Gemini Ready)" : "Online (Set API Key)";
        }
    } catch (err) {
        document.getElementById("api-status-text").innerText = "Backend Offline";
        document.querySelector(".dot").className = "dot red";
    }
}

function setMode(mode) {
    currentMode = mode;
    document.getElementById("btn-universal").classList.toggle("active", mode === "universal");
    document.getElementById("btn-coding").classList.toggle("active", mode === "coding");

    const titleMap = {
        universal: "Universal Autonomous Agent Mode",
        coding: "Coding Developer Assistant Mode"
    };
    
    document.getElementById("current-mode-title").innerText = titleMap[mode] || "Universal Mode";
    document.getElementById("mode-badge").innerText = mode.toUpperCase();
}

function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendQuickPrompt(promptText) {
    document.getElementById("user-input").value = promptText;
    sendMessage();
}

async function sendMessage() {
    const textarea = document.getElementById("user-input");
    const message = textarea.value.strip ? textarea.value.trim() : textarea.value;
    
    if (!message) return;
    
    // Hide welcome card if present
    const welcomeCard = document.querySelector(".welcome-card");
    if (welcomeCard) welcomeCard.style.display = "none";
    
    // Render User Message Bubble
    appendMessage(message, "user");
    textarea.value = "";

    // Show Tool Activity Bar
    showToolActivity("apta AI is thinking & executing tools...");
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                mode: currentMode
            })
        });
        
        const data = await response.json();
        hideToolActivity();
        
        if (data.status === "success") {
            appendMessage(data.reply, "bot");
        } else {
            appendMessage("Mama, error occurred: " + (data.detail || "Server error"), "bot");
        }
    } catch (err) {
        hideToolActivity();
        appendMessage("Mama, server connection error! Make sure `python run_app.py` or `server.py` is running.", "bot");
    }
}

function appendMessage(text, sender) {
    const chatContainer = document.getElementById("chat-container");
    const msgBubble = document.createElement("div");
    msgBubble.className = `message-bubble ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${sender}-avatar`;
    avatar.innerText = sender === "user" ? "👤" : "🤖";

    const content = document.createElement("div");
    content.className = "content";

    if (sender === "bot") {
        content.innerHTML = marked.parse(text);
    } else {
        content.innerText = text;
    }

    msgBubble.appendChild(avatar);
    msgBubble.appendChild(content);
    chatContainer.appendChild(msgBubble);
    
    // Auto scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showToolActivity(text) {
    const bar = document.getElementById("tool-activity-bar");
    document.getElementById("tool-activity-text").innerText = text;
    bar.style.display = "flex";
}

function hideToolActivity() {
    document.getElementById("tool-activity-bar").style.display = "none";
}

function clearChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.innerHTML = `
        <div class="welcome-card">
            <div class="welcome-icon">🌐🤖</div>
            <h3>Namaste / Hello Mama! Nenu apta AI!</h3>
            <p>I am your Universal Autonomous AI Agent & Pair Programming Assistant created by Rajwanth Balaka.</p>
        </div>
    `;
}
