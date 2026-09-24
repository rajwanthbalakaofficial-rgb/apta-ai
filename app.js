/* ==========================================================================
   apta AI - Universal Application Engine JavaScript (Hybrid Local & Web Client)
   ========================================================================== */

let currentMode = "universal";
const API_BASE_URL = "http://localhost:8000";

const SYSTEM_PROMPTS = {
    universal: `You are apta AI (ఆప్త AI), a standalone Universal Autonomous AI Agent & Pair Programming Assistant created by Rajwanth Balaka.
You operate across software development, writing, research, and project engineering.
Communicate warmly in Teluglish (Tanglish - Telugu written in English script), Telugu, or English based on user preference.`,
    coding: `You are apta AI, an intelligent AI Coding Assistant created by Rajwanth Balaka. Provide accurate code, debugging, and advice in Teluglish or English.`
};

document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    initKeyModal();
});

function initKeyModal() {
    const savedKey = localStorage.getItem("APTA_GEMINI_KEY") || "";
    if (savedKey) {
        document.getElementById("api-status-text").innerText = "Web Live (Gemini Ready)";
    }
}

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/health`, { signal: AbortSignal.timeout(2000) });
        const data = await res.json();
        const statusElem = document.getElementById("api-status-text");
        if (data.status === "online") {
            statusElem.innerText = data.gemini_status === "configured" ? "Local Backend (Gemini Ready)" : "Local Backend (Set Key)";
            document.querySelector(".dot").className = "dot green";
            return;
        }
    } catch (err) {
        const savedKey = localStorage.getItem("APTA_GEMINI_KEY");
        const statusElem = document.getElementById("api-status-text");
        if (savedKey) {
            statusElem.innerText = "Web Client (Gemini Active)";
            document.querySelector(".dot").className = "dot green";
        } else {
            statusElem.innerText = "Web Client (Key Required)";
            document.querySelector(".dot").className = "dot yellow";
        }
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

function promptApiKey() {
    const currentKey = localStorage.getItem("APTA_GEMINI_KEY") || "";
    const key = prompt("Mama, Enter your Gemini API Key to enable direct Web Chat:", currentKey);
    if (key !== null) {
        localStorage.setItem("APTA_GEMINI_KEY", key.trim());
        checkHealth();
        alert("Gemini API Key saved! Now you can chat directly in the browser.");
    }
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
    const message = textarea.value.trim();
    
    if (!message) return;
    
    const welcomeCard = document.querySelector(".welcome-card");
    if (welcomeCard) welcomeCard.style.display = "none";
    
    appendMessage(message, "user");
    textarea.value = "";

    showToolActivity("apta AI is thinking & generating response...");
    
    // Try Local Backend First
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message, mode: currentMode }),
            signal: AbortSignal.timeout(3000)
        });
        
        const data = await response.json();
        hideToolActivity();
        
        if (data.status === "success") {
            appendMessage(data.reply, "bot");
            return;
        }
    } catch (err) {
        // Fall back to Direct Browser Gemini API
    }

    // Direct Browser Gemini Call
    let apiKey = localStorage.getItem("APTA_GEMINI_KEY");
    if (!apiKey) {
        hideToolActivity();
        apiKey = prompt("Mama, Browser lo direct ga chat cheyaniki mee Gemini API Key ivvandi (Saved locally in browser):");
        if (apiKey) {
            apiKey = apiKey.trim();
            localStorage.setItem("APTA_GEMINI_KEY", apiKey);
            showToolActivity("Connecting to Gemini API...");
        } else {
            appendMessage("Mama, Web UI is live! Please set your Gemini API Key using the Key button at the top or start local backend with `python run_app.py`.", "bot");
            return;
        }
    }

    try {
        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
        const sysInstruction = SYSTEM_PROMPTS[currentMode] || SYSTEM_PROMPTS.universal;

        const res = await fetch(geminiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                system_instruction: { parts: [{ text: sysInstruction }] },
                contents: [{ parts: [{ text: message }] }]
            })
        });

        const data = await res.json();
        hideToolActivity();

        if (data.candidates && data.candidates[0].content.parts[0].text) {
            const botReply = data.candidates[0].content.parts[0].text;
            appendMessage(botReply, "bot");
        } else if (data.error) {
            appendMessage(`Mama, API Error: ${data.error.message}`, "bot");
        } else {
            appendMessage("Mama, Gemini returned an empty response. Try asking again!", "bot");
        }
    } catch (e) {
        hideToolActivity();
        appendMessage(`Mama, API call failed: ${e.message}. Check your API Key!`, "bot");
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
