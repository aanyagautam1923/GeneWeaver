"use strict";

/* ==========================================
   GeneWeaver Frontend Application
   ========================================== */

const API_BASE_URL = "http://127.0.0.1:8000";

const API_ENDPOINTS = {
    health: "/health",
    sequenceAnalysis: "/sequence/analyze",
    alignment: "/alignment",
    pamDetection: "/pam/detect",
    systemStatus: "/system/status"
};


/* ==========================================
   DOM Helpers
   ========================================== */

function getElement(id) {
    return document.getElementById(id);
}

function showMessage(elementId, message) {
    const element = getElement(elementId);

    if (element) {
        element.innerHTML = `<p>${escapeHTML(message)}</p>`;
    }
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);
}

function setLoading(buttonId, loading) {
    const button = getElement(buttonId);

    if (!button) return;

    button.disabled = loading;
    button.dataset.originalText ??= button.textContent;
    button.textContent = loading
        ? "Processing..."
        : button.dataset.originalText;
}

function renderResult(elementId, title, data) {
    const container = getElement(elementId);

    if (!container) return;

    const rows = Object.entries(data)
        .map(([key, value]) => {
            const displayValue =
                typeof value === "object" && value !== null
                    ? JSON.stringify(value)
                    : String(value);

            return `
                <div class="result-row">
                    <strong>${escapeHTML(key.replaceAll("_", " "))}</strong>
                    <span>${escapeHTML(displayValue)}</span>
                </div>
            `;
        })
        .join("");

    container.innerHTML = `
        <h3>${escapeHTML(title)}</h3>
        ${rows || "<p>No results returned.</p>"}
    `;
}


/* ==========================================
   API Communication
   ========================================== */

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {
        const message =
            data.detail ||
            data.message ||
            `Request failed with status ${response.status}`;

        throw new Error(
            typeof message === "string"
                ? message
                : JSON.stringify(message)
        );
    }

    return data;
}


/* ==========================================
   Backend Health Check
   ========================================== */

async function checkBackendHealth() {
    const statusElement = getElement("backendStatus");
    const healthElement = getElement("backendHealth");
    const apiElement = getElement("apiStatus");

    try {
        const data = await apiRequest(API_ENDPOINTS.health);

        if (statusElement) {
            statusElement.innerHTML =
                '<span class="status-dot"></span> Backend Connected';
        }

        if (healthElement) {
            healthElement.textContent = "Online";
        }

        if (apiElement) {
            apiElement.textContent = "Connected";
        }

        return data;

    } catch (error) {
        if (statusElement) {
            statusElement.textContent = "Backend Offline";
        }

        if (healthElement) {
            healthElement.textContent = "Offline";
        }

        if (apiElement) {
            apiElement.textContent = "Disconnected";
        }

        console.warn("Backend connection:", error.message);

        return null;
    }
}


/* ==========================================
   Sequence Length Counter
   ========================================== */

function initializeSequenceCounter() {
    const input = getElement("dnaSequence");
    const counter = getElement("sequenceLength");

    if (!input || !counter) return;

    input.addEventListener("input", () => {
        const sequence = input.value.replace(/\s/g, "");

        counter.textContent =
            `${sequence.length} nucleotides`;
    });
}


/* ==========================================
   DNA Sequence Validation
   ========================================== */

function validateDNA(sequence) {
    const normalized = sequence
        .toUpperCase()
        .replace(/\s/g, "");

    if (!normalized) {
        throw new Error("Please enter a DNA sequence.");
    }

    if (!/^[ATGCN]+$/.test(normalized)) {
        throw new Error(
            "Invalid DNA sequence. Only A, T, G, C and N are allowed."
        );
    }

    return normalized;
}


/* ==========================================
   Sequence Analysis
   ========================================== */

async function analyzeSequence() {
    const buttonId = "analyzeBtn";
    setLoading(buttonId, true);

    try {
        const sequence = validateDNA(
            getElement("dnaSequence").value
        );

        const data = await apiRequest(
            API_ENDPOINTS.sequenceAnalysis,
            {
                method: "POST",
                body: JSON.stringify({ sequence })
            }
        );

        renderResult(
            "analysisResults",
            "Sequence Analysis Results",
            data
        );

        updateAnalysisCount();

    } catch (error) {
        showMessage("analysisResults", error.message);
    } finally {
        setLoading(buttonId, false);
    }
}


/* ==========================================
   DNA Alignment
   ========================================== */

async function runAlignment() {
    const buttonId = "alignBtn";
    setLoading(buttonId, true);

    try {
        const sequenceA = validateDNA(
            getElement("sequenceA").value
        );

        const sequenceB = validateDNA(
            getElement("sequenceB").value
        );

        const data = await apiRequest(
            API_ENDPOINTS.alignment,
            {
                method: "POST",
                body: JSON.stringify({
                    sequence_a: sequenceA,
                    sequence_b: sequenceB
                })
            }
        );

        renderResult(
            "alignmentResults",
            "Alignment Results",
            data
        );

        updateAnalysisCount();

    } catch (error) {
        showMessage("alignmentResults", error.message);
    } finally {
        setLoading(buttonId, false);
    }
}


/* ==========================================
   PAM Detection
   ========================================== */

async function detectPAM() {
    const buttonId = "pamBtn";
    setLoading(buttonId, true);

    try {
        const sequence = validateDNA(
            getElement("pamSequence").value
        );

        const data = await apiRequest(
            API_ENDPOINTS.pamDetection,
            {
                method: "POST",
                body: JSON.stringify({
                    sequence,
                    pam_pattern: "NGG",
                    guide_length: 20
                })
            }
        );

        renderResult(
            "pamResults",
            "PAM Detection Results",
            data
        );

        updateAnalysisCount();

    } catch (error) {
        showMessage("pamResults", error.message);
    } finally {
        setLoading(buttonId, false);
    }
}


/* ==========================================
   Dashboard Statistics
   ========================================== */

let analysisCount = 0;

function updateAnalysisCount() {
    analysisCount++;

    const element = getElement("analysisCount");

    if (element) {
        element.textContent = analysisCount;
    }
}

async function loadSystemStatus() {
    try {
        const data = await apiRequest(API_ENDPOINTS.systemStatus);

        const mode = data.processing_mode || "Unknown";

        if (getElement("processingMode")) {
            getElement("processingMode").textContent = mode;
        }

        if (getElement("performanceMode")) {
            getElement("performanceMode").textContent = mode;
        }

        if (getElement("gpuStatus")) {
            getElement("gpuStatus").textContent =
                data.gpu_available ? "Available" : "Unavailable";
        }

    } catch (error) {
        console.warn("System status unavailable:", error.message);

        if (getElement("processingMode")) {
            getElement("processingMode").textContent = "Unknown";
        }

        if (getElement("performanceMode")) {
            getElement("performanceMode").textContent = "Unknown";
        }

        if (getElement("gpuStatus")) {
            getElement("gpuStatus").textContent = "Not Connected";
        }
    }
}


/* ==========================================
   Sidebar Navigation
   ========================================== */

function initializeNavigation() {
    const links = document.querySelectorAll(".nav-link");

    links.forEach(link => {
        link.addEventListener("click", () => {
            links.forEach(item => item.classList.remove("active"));
            link.classList.add("active");
        });
    });
}


/* ==========================================
   Event Listeners
   ========================================== */

function initializeApplication() {
    getElement("analyzeBtn")?.addEventListener(
        "click",
        analyzeSequence
    );

    getElement("alignBtn")?.addEventListener(
        "click",
        runAlignment
    );

    getElement("pamBtn")?.addEventListener(
        "click",
        detectPAM
    );

    initializeSequenceCounter();
    initializeNavigation();

    checkBackendHealth();
    loadSystemStatus();

    console.log("GeneWeaver frontend initialized.");
}


/* ==========================================
   Application Start
   ========================================== */

document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);
