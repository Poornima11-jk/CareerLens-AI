const fileInput = document.getElementById("resume-file");
const button = document.getElementById("upload-btn");
const message = document.getElementById("message");
const result = document.getElementById("result");
const summary = document.getElementById("result-summary");
const detectedList = document.getElementById("detected-list");
const notDetectedSummary = document.getElementById("not-detected-summary");
const notDetectedList = document.getElementById("not-detected-list");

const MAX_BYTES = 5 * 1024 * 1024; // 5 MB, same limit as the server

function showMessage(text, type) {
  message.textContent = text;
  message.className = "message " + type;
}

function makeChip(text, className, title) {
  const chip = document.createElement("span");
  chip.className = "chip " + className;
  chip.textContent = text;
  if (title) chip.title = title;
  return chip;
}

function renderDetected(detected) {
  detectedList.replaceChildren();

  if (detected.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "No skills from our list were detected in this resume.";
    detectedList.appendChild(empty);
    return;
  }

  const groups = {};
  detected.forEach((skill) => {
    (groups[skill.category] = groups[skill.category] || []).push(skill);
  });

  Object.keys(groups).forEach((category) => {
    const heading = document.createElement("h3");
    heading.textContent = category;
    const row = document.createElement("div");
    row.className = "chips";
    groups[category].forEach((skill) => {
      const evidence = "Matched as: " + skill.matched_as.join(", ");
      row.appendChild(makeChip(skill.name, "chip-found", evidence));
    });
    detectedList.append(heading, row);
  });
}

function renderNotDetected(names) {
  notDetectedList.replaceChildren();
  notDetectedSummary.textContent = "Not detected (" + names.length + " skills from our list)";
  names.forEach((name) => notDetectedList.appendChild(makeChip(name, "chip-missing")));
}

button.addEventListener("click", async () => {
  result.hidden = true;
  const file = fileInput.files[0];

  if (!file) {
    showMessage("Please choose a PDF file first.", "error");
    return;
  }
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showMessage("Please upload a PDF file (.pdf).", "error");
    return;
  }
  if (file.size > MAX_BYTES) {
    showMessage("The file is too large. Maximum size is 5 MB.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  button.disabled = true;
  showMessage("Analyzing your resume...", "info");

  try {
    const response = await fetch("/api/resume/analyze", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (!response.ok) {
      const text = typeof data.detail === "string" ? data.detail : "Something went wrong.";
      showMessage(text, "error");
      return;
    }

    showMessage("Resume analyzed.", "success");
    summary.textContent =
      data.filename + " — " + data.characters + " characters read, " +
      data.detected.length + " skills detected.";
    renderDetected(data.detected);
    renderNotDetected(data.not_detected);
    result.hidden = false;
  } catch (error) {
    showMessage("Could not reach the server. Check your connection and try again.", "error");
  } finally {
    button.disabled = false;
  }
});