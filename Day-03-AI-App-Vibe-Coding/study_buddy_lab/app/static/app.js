// app.js - connects the web page to the Study Buddy API.
// Safety rule: we put text on the page with textContent (never innerHTML),
// so text from documents or from the AI cannot run as code in the browser.

const $ = (id) => document.getElementById(id);

// Small helper: call the API and return JSON, or throw an Error with the server's message
async function callApi(url, options = {}) {
  const response = await fetch(url, options);
  let body = {};
  try { body = await response.json(); } catch (e) { /* no JSON body */ }
  if (!response.ok) {
    const detail = Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join("; ") : body.detail;
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return body;
}

function postJson(url, data) {
  return callApi(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
}

function show(element, text, isError = false) {
  element.textContent = text;
  element.classList.toggle("error", isError);
}

// Disable a button while waiting, so users do not click twice
async function busy(button, work) {
  button.disabled = true;
  try { await work(); } finally { button.disabled = false; }
}

function modeNote(mode) {
  return mode === "mock" ? "\n\n[MOCK MODE: pretend AI answer. Add an API key for real answers.]" : "";
}

// ---- Status and document list ----------------------------------------------
async function refreshStatus() {
  try {
    const health = await callApi("/health");
    show($("status"), `Server OK. AI mode: ${health.ai_mode}. Documents: ${health.documents}.`);
  } catch (error) {
    show($("status"), "Cannot reach the server. Is uvicorn running?", true);
  }
}

async function refreshDocuments() {
  const data = await callApi("/api/documents");
  const list = $("doc-list");
  list.replaceChildren();
  for (const doc of data.documents) {
    const item = document.createElement("li");
    item.textContent = `${doc.filename} (${doc.chunks} chunks)`;
    list.appendChild(item);
  }
  refreshStatus();
}

// ---- 1. Upload ---------------------------------------------------------------
$("upload-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const button = event.submitter;
  busy(button, async () => {
    const form = new FormData();
    form.append("file", $("doc-file").files[0]);
    try {
      const result = await callApi("/api/documents", { method: "POST", body: form });
      show($("upload-result"), `Uploaded ${result.filename}: ${result.characters} characters, ${result.chunks} chunks.`);
      refreshDocuments();
    } catch (error) {
      show($("upload-result"), error.message, true);
    }
  });
});

$("clear-docs").addEventListener("click", async () => {
  await callApi("/api/documents", { method: "DELETE" });
  show($("upload-result"), "All documents removed.");
  refreshDocuments();
});

// ---- 2. Ask ------------------------------------------------------------------
$("ask-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    show($("answer"), "Thinking...");
    $("sources").replaceChildren();
    try {
      const result = await postJson("/api/ask", { question: $("question").value });
      show($("answer"), result.answer + modeNote(result.mode));
      for (const source of result.sources) {
        const item = document.createElement("li");
        item.textContent = `${source.source} (score ${source.score}): ${source.text.slice(0, 200)}...`;
        $("sources").appendChild(item);
      }
    } catch (error) {
      show($("answer"), error.message, true);
    }
  });
});

// ---- 3. Summary and practice questions ---------------------------------------
$("summary-btn").addEventListener("click", (event) => {
  busy(event.target, async () => {
    show($("study-result"), "Summarising...");
    try {
      const result = await postJson("/api/summary", { count: 5 });
      show($("study-result"), result.summary + modeNote(result.mode));
    } catch (error) {
      show($("study-result"), error.message, true);
    }
  });
});

$("practice-btn").addEventListener("click", (event) => {
  busy(event.target, async () => {
    show($("study-result"), "Creating questions...");
    try {
      const result = await postJson("/api/practice-questions", { count: 5 });
      const text = result.questions.map((q, i) => `Q${i + 1}. ${q.question}\nAnswer: ${q.answer}`).join("\n\n");
      show($("study-result"), text + modeNote(result.mode));
    } catch (error) {
      show($("study-result"), error.message, true);
    }
  });
});

// ---- 4. CSV ------------------------------------------------------------------
$("csv-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const form = new FormData();
    form.append("file", $("csv-file").files[0]);
    if ($("csv-column").value.trim()) form.append("column", $("csv-column").value.trim());
    show($("csv-result"), "Analysing...");
    $("csv-chart").hidden = true;
    try {
      const result = await callApi("/api/csv", { method: "POST", body: form });
      const text = `Columns: ${result.columns.join(", ")}\n\nFacts:\n- ${result.insights.join("\n- ")}\n\nExplanation:\n${result.explanation}`;
      show($("csv-result"), text + modeNote(result.mode));
      $("csv-chart").src = `data:image/png;base64,${result.chart_png_base64}`;
      $("csv-chart").hidden = false;
    } catch (error) {
      show($("csv-result"), error.message, true);
    }
  });
});

// ---- 5. OCR ------------------------------------------------------------------
$("ocr-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const form = new FormData();
    form.append("file", $("ocr-file").files[0]);
    form.append("add_to_documents", $("ocr-add").checked);
    show($("ocr-result"), "Reading...");
    try {
      const result = await callApi("/api/ocr", { method: "POST", body: form });
      show($("ocr-result"), result.text || "(no text found)");
      if (result.added_to_documents) refreshDocuments();
    } catch (error) {
      show($("ocr-result"), error.message, true);
    }
  });
});

// ---- 6. Agent ----------------------------------------------------------------
$("agent-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    $("agent-steps").replaceChildren();
    show($("agent-result"), "Working...");
    try {
      const result = await postJson("/api/agent", { goal: $("goal").value });
      for (const step of result.steps) {
        const item = document.createElement("li");
        item.textContent = `${step.tool}("${step.input}") -> ${step.observation.slice(0, 200)}`;
        $("agent-steps").appendChild(item);
      }
      show($("agent-result"), "Final answer: " + result.final_answer + modeNote(result.mode));
    } catch (error) {
      show($("agent-result"), error.message, true);
    }
  });
});

refreshDocuments();
