"use strict";

const API_BASE_URL = "http://127.0.0.1:8000";

const API_ENDPOINTS = {
    health: "/health",
    sequenceAnalysis: "/sequence/analyze",
    alignment: "/alignment",
    pamDetection: "/pam/detect",
    systemStatus: "/system/status",
    search: "/search/"
};

function getElement(id) {
    return document.getElementById(id);
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;",
        '"': "&quot;", "'": "&#039;"
    })[c]);
}

function showMessage(id, message) {
    const el = getElement(id);
    if (el) el.innerHTML = `<p>${escapeHTML(message)}</p>`;
}

function setLoading(id, loading) {
    const btn = getElement(id);
    if (!btn) return;
    btn.disabled = loading;
    btn.dataset.originalText ??= btn.textContent;
    btn.textContent = loading ? "Processing..." : btn.dataset.originalText;
}

function renderResult(id, title, data) {
    const container = getElement(id);
    if (!container) return;

    const rows = Object.entries(data || {}).map(([key, value]) => `
        <div class="result-row">
            <strong>${escapeHTML(key.replaceAll("_", " "))}</strong>
            <span>${escapeHTML(typeof value === "object" ? JSON.stringify(value) : value)}</span>
        </div>
    `).join("");

    container.innerHTML = `<h3>${escapeHTML(title)}</h3>${rows || "<p>No results.</p>"}`;
}

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || `HTTP ${response.status}`);
    }
    return data;
}

function validateDNA(raw) {
    const seq = String(raw || "").toUpperCase().replace(/\s/g, "");
    if (!seq) throw new Error("DNA sequence is required.");
    if (!/^[ATGCN]+$/.test(seq)) throw new Error("Only A, T, G, C, N are allowed.");
    return seq;
}

async function checkBackendHealth() {
    try {
        await apiRequest(API_ENDPOINTS.health);
        if (getElement("backendStatus")) getElement("backendStatus").textContent = "Backend Connected";
        if (getElement("backendHealth")) getElement("backendHealth").textContent = "Online";
        if (getElement("apiStatus")) getElement("apiStatus").textContent = "Connected";
        return true;
    } catch {
        if (getElement("backendStatus")) getElement("backendStatus").textContent = "Backend Offline";
        if (getElement("backendHealth")) getElement("backendHealth").textContent = "Offline";
        if (getElement("apiStatus")) getElement("apiStatus").textContent = "Disconnected";
        return false;
    }
}

let analysisCount = 0;
function updateAnalysisCount() {
    analysisCount++;
    if (getElement("analysisCount")) getElement("analysisCount").textContent = analysisCount;
}

async function analyzeSequence() {
    setLoading("analyzeBtn", true);
    try {
        const sequence = validateDNA(getElement("dnaSequence").value);
        const data = await apiRequest(API_ENDPOINTS.sequenceAnalysis, {
            method: "POST", body: JSON.stringify({sequence})
        });
        renderResult("analysisResults", "Sequence Analysis Results", data.data || data);
        saveHistory("Sequence Analysis", sequence);
        updateAnalysisCount();
    } catch (e) {
        showMessage("analysisResults", e.message);
    } finally {
        setLoading("analyzeBtn", false);
    }
}

async function runAlignment() {
    setLoading("alignBtn", true);
    try {
        const sequence_a = validateDNA(getElement("sequenceA").value);
        const sequence_b = validateDNA(getElement("sequenceB").value);
        const data = await apiRequest(API_ENDPOINTS.alignment, {
            method: "POST", body: JSON.stringify({sequence_a, sequence_b})
        });
        renderResult("alignmentResults", "Alignment Results", data.data || data);
        saveHistory("Alignment", `${sequence_a} | ${sequence_b}`);
        updateAnalysisCount();
    } catch (e) {
        showMessage("alignmentResults", e.message);
    } finally {
        setLoading("alignBtn", false);
    }
}

async function detectPAM() {
    setLoading("pamBtn", true);
    try {
        const sequence = validateDNA(getElement("pamSequence").value);
        const data = await apiRequest(API_ENDPOINTS.pamDetection, {
            method: "POST",
            body: JSON.stringify({sequence, pam_pattern: "NGG", guide_length: 20})
        });
        renderResult("pamResults", "PAM Detection Results", data.data || data);
        saveHistory("PAM Detection", sequence);
        updateAnalysisCount();
    } catch (e) {
        showMessage("pamResults", e.message);
    } finally {
        setLoading("pamBtn", false);
    }
}

async function searchDNA() {
    const sequence = getElement("dnaSequence")?.value;
    const query = prompt("Enter DNA query sequence:");
    if (!query) return;

    try {
        const data = await apiRequest(API_ENDPOINTS.search, {
            method: "POST",
            body: JSON.stringify({
                reference: validateDNA(sequence),
                query: validateDNA(query),
                max_mismatches: 0,
                both_strands: true
            })
        });
        renderResult("analysisResults", "Sequence Search Results", data.data || data);
        saveHistory("Sequence Search", sequence);
        updateAnalysisCount();
    } catch (e) {
        showMessage("analysisResults", e.message);
    }
}

function saveHistory(type, sequence) {
    const history = JSON.parse(localStorage.getItem("geneweaver_history") || "[]");
    history.unshift({type, sequence: sequence.slice(0, 80), date: new Date().toLocaleString()});
    localStorage.setItem("geneweaver_history", JSON.stringify(history.slice(0, 30)));
    loadHistory();
}

function loadHistory() {
    const container = getElement("historyResults");
    if (!container) return;
    const history = JSON.parse(localStorage.getItem("geneweaver_history") || "[]");
    if (!history.length) {
        container.innerHTML = "<p>No analysis history yet.</p>";
        return;
    }
    container.innerHTML = history.map(item => `
        <div class="result-row">
            <strong>${escapeHTML(item.type)}</strong>
            <span>${escapeHTML(item.date)}<br>${escapeHTML(item.sequence)}</span>
        </div>
    `).join("");
}

function calculateGC(sequence) {
    const seq = validateDNA(sequence);
    const gc = [...seq].filter(b => b === "G" || b === "C").length;
    return ((gc / seq.length) * 100).toFixed(2);
}

function reverseComplement(sequence) {
    return validateDNA(sequence).split("").reverse().map(b => ({
        A: "T", T: "A", G: "C", C: "G", N: "N"
    })[b]).join("");
}

async function loadSystemStatus() {
    try {
        const response = await apiRequest(API_ENDPOINTS.systemStatus);
        const data = response.data || response;
        const mode = data.processing_mode || "Unknown";
        if (getElement("processingMode")) getElement("processingMode").textContent = mode;
        if (getElement("performanceMode")) getElement("performanceMode").textContent = mode;
        if (getElement("gpuStatus")) getElement("gpuStatus").textContent = data.gpu_available ? "Available" : "Unavailable";
    } catch {
        if (getElement("processingMode")) getElement("processingMode").textContent = "Unknown";
        if (getElement("performanceMode")) getElement("performanceMode").textContent = "Unknown";
        if (getElement("gpuStatus")) getElement("gpuStatus").textContent = "Unavailable";
    }
}

function initializeSequenceCounter() {
    const input = getElement("dnaSequence");
    const counter = getElement("sequenceLength");
    if (!input || !counter) return;
    input.addEventListener("input", () => {
        counter.textContent = `${input.value.replace(/\s/g, "").length} nucleotides`;
    });
}

function initializeNavigation() {
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            document.querySelectorAll(".nav-link").forEach(x => x.classList.remove("active"));
            link.classList.add("active");
        });
    });
}

function initializeApplication() {
    getElement("analyzeBtn")?.addEventListener("click", analyzeSequence);
    getElement("alignBtn")?.addEventListener("click", runAlignment);
    getElement("pamBtn")?.addEventListener("click", detectPAM);
    initializeSequenceCounter();
    initializeNavigation();
    loadHistory();
    checkBackendHealth();
    loadSystemStatus();
    setInterval(checkBackendHealth, 10000);
    setInterval(loadSystemStatus, 15000);
    console.log("GeneWeaver connected frontend initialized.");
}

document.addEventListener("DOMContentLoaded", () => { initializeApplication(); initializeSequenceTools(); });


// ===== GENEWEAVER SEQUENCE TOOLS =====
function initializeSequenceTools() {
    const section = document.getElementById("sequence-tools");
    if (!section || document.getElementById("sequenceToolsPanel")) return;

    const panel = document.createElement("div");
    panel.id = "sequenceToolsPanel";
    panel.style.cssText = "margin-top:24px;padding:20px;border:1px solid var(--border-color,#ddd);border-radius:14px;";

    panel.innerHTML = `
        <h3>DNA Utility Workbench</h3>
        <p>Enter DNA sequence to use the bioinformatics tools.</p>
        <textarea id="toolsDNA" rows="5" placeholder="Enter DNA sequence (A, T, G, C)..." style="width:100%;box-sizing:border-box;padding:12px;"></textarea>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin:14px 0;">
            <button class="primary-btn" id="gcToolBtn">GC Content</button>
            <button class="primary-btn" id="tmToolBtn">Melting Temperature</button>
            <button class="primary-btn" id="rcToolBtn">Reverse Complement</button>
        </div>
        <hr>
        <h3>Multi-FASTA Analyzer</h3>
        <textarea id="multiFastaInput" rows="7" placeholder=">Sequence_1&#10;ATGCATGC&#10;>Sequence_2&#10;GCGCGCAA" style="width:100%;box-sizing:border-box;padding:12px;"></textarea>
        <button class="primary-btn" id="fastaToolBtn" style="margin-top:12px;">Analyze FASTA Records</button>
        <div id="sequenceToolsOutput" class="results-container" style="margin-top:16px;"></div>
    `;

    section.appendChild(panel);

    const output = document.getElementById("sequenceToolsOutput");

    function getDNA() {
        const sequence = document.getElementById("toolsDNA").value.toUpperCase().replace(/\s/g, "");
        if (!sequence) {
            output.innerHTML = "<p>Please enter a DNA sequence first.</p>";
            return null;
        }
        if (!/^[ATGC]+$/.test(sequence)) {
            output.innerHTML = "<p>Invalid DNA. Only A, T, G, C characters are allowed.</p>";
            return null;
        }
        return sequence;
    }

    document.getElementById("gcToolBtn").onclick = () => {
        const dna = getDNA();
        if (!dna) return;
        const gc = ((dna.match(/[GC]/g) || []).length / dna.length) * 100;
        output.innerHTML = `<h4>GC Content Result</h4><p>Length: ${dna.length} bp</p><p>GC Content: ${gc.toFixed(2)}%</p><p>AT Content: ${(100-gc).toFixed(2)}%</p>`;
    };

    document.getElementById("tmToolBtn").onclick = () => {
        const dna = getDNA();
        if (!dna) return;
        const a = (dna.match(/A/g) || []).length;
        const t = (dna.match(/T/g) || []).length;
        const g = (dna.match(/G/g) || []).length;
        const c = (dna.match(/C/g) || []).length;
        const tm = dna.length < 14 ? 2*(a+t)+4*(g+c) : 64.9 + 41*(g+c-16.4)/dna.length;
        output.innerHTML = `<h4>Estimated Melting Temperature</h4><p>Length: ${dna.length} bp</p><p>Tm: ${tm.toFixed(2)} °C</p><small>Estimate only; actual Tm depends on salt, concentration and experimental conditions.</small>`;
    };

    document.getElementById("rcToolBtn").onclick = () => {
        const dna = getDNA();
        if (!dna) return;
        const complement = {A:"T", T:"A", G:"C", C:"G"};
        const result = [...dna].reverse().map(base => complement[base]).join("");
        output.innerHTML = `<h4>Reverse Complement</h4><p>Length: ${result.length} bp</p><textarea rows="4" readonly style="width:100%;box-sizing:border-box;">${result}</textarea><button id="copyRCBtn" class="primary-btn">Copy Sequence</button>`;
        document.getElementById("copyRCBtn").onclick = async () => {
            try {
                await navigator.clipboard.writeText(result);
                document.getElementById("copyRCBtn").textContent = "Copied!";
            } catch {
                output.insertAdjacentHTML("beforeend", "<p>Clipboard access unavailable. Select and copy the sequence manually.</p>");
            }
        };
    };

    document.getElementById("fastaToolBtn").onclick = () => {
        const text = document.getElementById("multiFastaInput").value.trim();
        if (!text) {
            output.innerHTML = "<p>Please paste FASTA records.</p>";
            return;
        }
        const records = [];
        let header = "";
        let seq = "";

        for (const line of text.split(/\r?\n/)) {
            const trimmed = line.trim();
            if (!trimmed) continue;
            if (trimmed.startsWith(">")) {
                if (header) records.push({header, sequence:seq});
                header = trimmed.slice(1).trim();
                seq = "";
            } else {
                if (!header) {
                    output.innerHTML = "<p>Invalid FASTA: sequence header must start with &gt;.</p>";
                    return;
                }
                seq += trimmed.replace(/\s/g, "").toUpperCase();
            }
        }
        if (header) records.push({header, sequence:seq});

        if (!records.length || records.some(r => !r.sequence || !/^[ATGC]+$/.test(r.sequence))) {
            output.innerHTML = "<p>FASTA contains an empty sequence or invalid DNA characters.</p>";
            return;
        }

        output.innerHTML = `<h4>FASTA Analysis — ${records.length} records</h4>` + records.map(r => {
            const gc = ((r.sequence.match(/[GC]/g) || []).length/r.sequence.length)*100;
            return `<div style="padding:10px;margin:8px 0;border:1px solid #ddd;border-radius:8px;"><strong>${escapeHTML(r.header)}</strong><p>Length: ${r.sequence.length} bp | GC: ${gc.toFixed(2)}%</p></div>`;
        }).join("");
    };
}

