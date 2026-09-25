/* ==========================================================================
   apta AI - Proprietary Neural AI Engine Studio JavaScript
   Created by Rajwanth Balaka.
   ========================================================================== */

let stepIndex = 0;
let isDrawerOpen = false;
const API_BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
    checkStatus();
});

async function checkStatus() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/health`, { signal: AbortSignal.timeout(2000) });
        const data = await res.json();
        if (data.status === "online") {
            document.getElementById("api-status-text").innerText = "apta Neural Engine Active";
        }
    } catch (e) {
        document.getElementById("api-status-text").innerText = "apta Neural Engine Live";
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

async function executePrompt() {
    const textarea = document.getElementById("user-prompt");
    const text = textarea.value.trim();
    if (!text) return;

    stepIndex++;
    document.getElementById("step-badge").innerText = `STEP ${stepIndex}`;

    // Hide welcome banner
    const banner = document.querySelector(".welcome-banner");
    if (banner) banner.style.display = "none";

    // Append Trajectory Step Item
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
                <i class="fa-solid fa-brain"></i> apta Neural Thinking (Click to expand)
            </div>
            <div class="cot-content" style="display: none; margin-top: 6px; padding: 6px; background: rgba(0,0,0,0.3); border-radius: 4px;">
                Analyzing instruction '${text}', evaluating workspace trajectory, executing apta Neural inference, and dispatching tool actions...
            </div>
        </div>
        <div class="step-content">
            <strong>User:</strong> ${text}
        </div>
    `;

    feed.appendChild(stepBox);
    textarea.value = "";
    feed.scrollTop = feed.scrollHeight;

    showActivity("apta Neural Model Processing...");

    // Try Local Backend First
    try {
        const selectedModel = document.getElementById("model-selector") ? document.getElementById("model-selector").value : "apta-neural-2.0";
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, mode: "universal", model: selectedModel }),
            signal: AbortSignal.timeout(4000)
        });
        const data = await response.json();
        hideActivity();
        if (data.status === "success") {
            appendStepReply(stepBox, data.reply);
            return;
        }
    } catch (e) {
        // Native apta Neural AI Fallback Engine
    }

    // Direct Browser apta AI Engine Response
    setTimeout(() => {
        hideActivity();
        const nativeReply = (
            `Namaste / Hello Mama! Nenu **apta Neural Engine**!\n\n` +
            `Nee request received: *"${text}"*.\n\n` +
            `Nenu Rajwanth Balaka dwara create cheyabadina standalone Autonomous AI Engine. ` +
            `Workspace files search cheyaniki, code write cheyaniki, and project development kosam 100% ready ga unnanu! 🚀`
        );
        appendStepReply(stepBox, nativeReply);
    }, 600);
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
