const fileInput = document.getElementById("resume-file");
const textArea = document.getElementById("job-text");
const button = document.getElementById("analyze-btn");
const message = document.getElementById("message");
const result = document.getElementById("result");

const MAX_BYTES = 5 * 1024 * 1024;

function showMessage(text, type) {
  message.textContent = text;
  message.className = "message " + type;
}

function fillChips(id, names, className, emptyText) {
  const box = document.getElementById(id);
  box.replaceChildren();
  if (names.length === 0) {
    const none = document.createElement("span");
    none.className = "none";
    none.textContent = emptyText;
    box.appendChild(none);
    return;
  }
  names.forEach((name) => {
    const chip = document.createElement("span");
    chip.className = "chip " + className;
    chip.textContent = name;
    box.appendChild(chip);
  });
}

function addItem(list, text) {
  const item = document.createElement("li");
  item.textContent = text;
  list.appendChild(item);
}

function renderScore(score) {
  const value = document.getElementById("score-value");
  value.textContent = score.overall === null ? "No score" : score.overall + "%";
  document.getElementById("score-method").textContent = "How it was calculated: " + score.method + ".";

  const parts = document.getElementById("score-parts");
  parts.replaceChildren();
  if (score.required_match !== null) addItem(parts, "Required skills matched: " + score.required_match + "%");
  if (score.preferred_match !== null) addItem(parts, "Preferred skills matched: " + score.preferred_match + "%");
  if (score.mentioned_match !== null) addItem(parts, "Mentioned skills matched: " + score.mentioned_match + "%");
  if (parts.children.length === 0) addItem(parts, "No recognised skills were found in the job description.");
}

function renderExperience(experience) {
  const list = document.getElementById("experience-list");
  list.replaceChildren();
  experience.matches.forEach((m) => {
    const years = m.max_years === null ? m.min_years + "+ years" : m.min_years + "–" + m.max_years + " years";
    addItem(list, years + " — from: \"" + m.line + "\"");
  });
  if (experience.entry_level) addItem(list, "Entry-level or fresher role mentioned.");
  if (list.children.length === 0) addItem(list, "Not detected");
}

function renderEducation(education) {
  const el = document.getElementById("education-text");
  if (education.levels.length > 0) el.textContent = education.levels.join(", ");
  else if (education.degree_mentioned) el.textContent = "A degree is mentioned, but no specific level was detected.";
  else el.textContent = "Not detected";
}

button.addEventListener("click", async () => {
  result.hidden = true;
  const file = fileInput.files[0];
  const jobText = textArea.value.trim();

  if (!file) { showMessage("Please choose a PDF file first.", "error"); return; }
  if (!file.name.toLowerCase().endsWith(".pdf")) { showMessage("Please upload a PDF file (.pdf).", "error"); return; }
  if (file.size > MAX_BYTES) { showMessage("The file is too large. Maximum size is 5 MB.", "error"); return; }
  if (!jobText) { showMessage("Please paste a job description.", "error"); return; }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_text", jobText);

  button.disabled = true;
  showMessage("Analyzing...", "info");

  try {
    const response = await fetch("/api/analyze", { method: "POST", body: formData });
    const data = await response.json();

    if (!response.ok) {
      showMessage(typeof data.detail === "string" ? data.detail : "Something went wrong.", "error");
      return;
    }

    showMessage("Analysis complete.", "success");
    renderScore(data.score);
    fillChips("strengths", data.gaps.strengths, "chip-found", "None");
    fillChips("gap-high", data.gaps.high, "chip-gap-high", "None");
    fillChips("gap-medium", data.gaps.medium, "chip-gap-medium", "None");
    fillChips("gap-low", data.gaps.low, "chip-missing", "None");
    fillChips("gap-unranked", data.gaps.unranked, "chip-missing", "None");
    renderExperience(data.experience);
    renderEducation(data.education);
    result.hidden = false;
  } catch (error) {
    showMessage("Could not reach the server. Check your connection and try again.", "error");
  } finally {
    button.disabled = false;
  }
});