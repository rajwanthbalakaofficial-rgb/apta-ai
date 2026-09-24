/* ==========================================================================
   apta AI - Antigravity Twin Studio Engine JavaScript (Robust Engine)
   ========================================================================== */

let stepIndex = 0;
let isDrawerOpen = false;
const API_BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
    try {
        if (typeof mermaid !== "undefined") {
            mermaid.initialize({ startOnLoad: true, theme: 'dark' });
        }
    } catch (e) {
        console.warn("Mermaid initialization deferred:", e);
    }
    checkStatus();
});

async function checkStatus() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/health`, { signal: AbortSignal.timeout(2000) });
        const data = await res.json();
        if (data.status === "online") {
            document.getElementById("api-status-text").innerText = "Antigravity Engine Active";
        }
    } catch (e) {
        const savedKey = localStorage.getItem("APTA_GEMINI_KEY");
        if (savedKey) {
            document.getElementById("api-status-text").innerText = "Studio Client (Gemini Ready)";
        } else {
            document.getElementById("api-status-text").innerText = "Studio Client (Set Key)";
        }
    }
}

function toggleArtifactDrawer() {
    const drawer = document.getElementById("artifact-drawer");
    isDrawerOpen = !isDrawerOpen;
    drawer.classList.toggle("open", isDrawerOpen);
}

function triggerSlashCommand(cmd) {
    document.getElementById("user-prompt").value = cmd + " ";
    document.getElementById("user-prompt").focus();
}

function handlePromptKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        executePrompt();
    }
}

function promptApiKey() {
    const key = prompt("Mama, Enter your Gemini API Key for direct Antigravity Studio execution:");
    if (key) {
        localStorage.setItem("APTA_GEMINI_KEY", key.trim());
        checkStatus();
        alert("API Key saved! Antigravity Studio is ready.");
    }
}

async function executePrompt() {
    const textarea = document.getElementById("user-prompt");
    const text = textarea.value.trim();
    if (!text) return;

    stepIndex++;
    document.getElementById("step-badge").innerText = `STEP ${stepIndex}`;

    // Hide banner
    const banner = document.querySelector(".welcome-banner");
    if (banner) banner.style.display = "none";

    // Append Trajectory Step Box
    const feed = document.getElementById("feed-container");
    const stepBox = document.createElement("div");
    stepBox.className = "trajectory-step";

    stepBox.innerHTML = `
        <div class="step-header">
            <span><i class="fa-solid fa-list-check"></i> STEP ${stepIndex}</span>
            <span>${new Date().toLocaleTimeString()}</span>
        </div>
        <div class="cot-drawer">
            <div class="cot-title" onclick="const c = this.nextElementSibling; c.style.display = c.style.display === 'none' ? 'block' : 'none';">
                <i class="fa-solid fa-brain"></i> Thinking / Chain-of-Thought Reasoning (Click to expand)
            </div>
            <div class="cot-content" style="display: none; margin-top: 6px; padding: 6px; background: rgba(0,0,0,0.3); border-radius: 4px;">
                Analyzing instruction '${text}', inspecting workspace trajectory, loading active skills (agy-customizations), and dispatching tool actions...
            </div>
        </div>
        <div class="step-content">
            <strong>User:</strong> ${text}
        </div>
    `;

    feed.appendChild(stepBox);
    textarea.value = "";
    feed.scrollTop = feed.scrollHeight;

    showActivity("Antigravity Execution in progress...");

    // Try Local Engine First
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, mode: "universal" }),
            signal: AbortSignal.timeout(3000)
        });
        const data = await response.json();
        hideActivity();
        if (data.status === "success") {
            appendStepReply(stepBox, data.reply);
            return;
        }
    } catch (e) {
        // Fallback to Browser Direct Gemini API
    }

    // Direct Browser Gemini API
    let apiKey = localStorage.getItem("APTA_GEMINI_KEY");
    if (!apiKey) {
        hideActivity();
        apiKey = prompt("Mama, Enter your Gemini API Key to run Antigravity Studio in Browser:");
        if (apiKey) {
            localStorage.setItem("APTA_GEMINI_KEY", apiKey.trim());
            apiKey = apiKey.trim();
        } else {
            appendStepReply(stepBox, "Mama, please provide a Gemini API Key to execute Antigravity Trajectory!");
            return;
        }
    }

    try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
        const sysInstruction = "You are apta AI, an exact Twin of the Google DeepMind Antigravity AI Coding Assistant created by Rajwanth Balaka. Respond warmly in Teluglish or English with step-by-step reasoning.";

        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                system_instruction: { parts: [{ text: sysInstruction }] },
                contents: [{ parts: [{ text: text }] }]
            })
        });

        const data = await res.json();
        hideActivity();

        if (data.candidates && data.candidates[0].content.parts[0].text) {
            appendStepReply(stepBox, data.candidates[0].content.parts[0].text);
        } else {
            appendStepReply(stepBox, "Mama, Gemini API error: " + (data.error ? data.error.message : "Empty response"));
        }
    } catch (err) {
        hideActivity();
        appendStepReply(stepBox, "Mama, execution failed: " + err.message);
    }
}

function appendStepReply(stepBox, replyText) {
    const replyElem = document.createElement("div");
    replyElem.style.marginTop = "12px";
    
    if (typeof marked !== "undefined") {
        replyElem.innerHTML = marked.parse(replyText);
    } else {
        replyElem.innerText = replyText;
    }
    
    stepBox.appendChild(replyElem);

    if (replyText.includes("Implementation Plan") || replyText.includes("# ")) {
        renderArtifact(replyText);
    }
}

function renderArtifact(content) {
    const drawerContent = document.getElementById("artifact-content");
    if (typeof marked !== "undefined") {
        drawerContent.innerHTML = marked.parse(content);
    } else {
        drawerContent.innerText = content;
    }
    if (!isDrawerOpen) toggleArtifactDrawer();
}

function showActivity(txt) {
    const t = document.getElementById("activity-toast");
    document.getElementById("activity-toast-text").innerText = txt;
    t.style.display = "flex";
}

function hideActivity() {
    document.getElementById("activity-toast").style.display = "none";
}
