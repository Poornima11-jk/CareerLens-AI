const fileInput = document.getElementById("resume-file");
const button = document.getElementById("upload-btn");
const message = document.getElementById("message");
const result = document.getElementById("result");
const summary = document.getElementById("result-summary");
const preview = document.getElementById("result-preview");

const MAX_BYTES = 5 * 1024 * 1024; // 5 MB, same limit as the server

function showMessage(text, type) {
  message.textContent = text;
  message.className = "message " + type;
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
  showMessage("Reading your resume...", "info");

  try {
    const response = await fetch("/api/resume/extract-text", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (!response.ok) {
      const text = typeof data.detail === "string" ? data.detail : "Something went wrong.";
      showMessage(text, "error");
      return;
    }

    showMessage("Resume read successfully.", "success");
    summary.textContent = data.filename + " — " + data.characters + " characters detected.";
    preview.textContent = data.preview;
    result.hidden = false;
  } catch (error) {
    showMessage("Could not reach the server. Check your connection and try again.", "error");
  } finally {
    button.disabled = false;
  }
});