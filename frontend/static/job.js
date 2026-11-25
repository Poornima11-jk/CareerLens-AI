const textArea = document.getElementById("job-text");
const button = document.getElementById("job-btn");
const message = document.getElementById("message");
const result = document.getElementById("result");
const summary = document.getElementById("result-summary");
const noHeadings = document.getElementById("no-headings");
const experienceList = document.getElementById("experience-list");
const educationText = document.getElementById("education-text");

function showMessage(text, type) {
  message.textContent = text;
  message.className = "message " + type;
}

function fillChips(id, names, emptyText) {
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
    chip.className = "chip chip-found";
    chip.textContent = name;
    box.appendChild(chip);
  });
}

function renderExperience(experience) {
  experienceList.replaceChildren();
  experience.matches.forEach((m) => {
    const item = document.createElement("li");
    const range = m.max_years === null ? m.min_years + "+ years" : m.min_years + "–" + m.max_years + " years";
    item.textContent = range + " — from: \"" + m.line + "\"";
    experienceList.appendChild(item);
  });
  if (experience.entry_level) {
    const item = document.createElement("li");
    item.textContent = "Entry-level or fresher role mentioned.";
    experienceList.appendChild(item);
  }
  if (experienceList.children.length === 0) {
    const item = document.createElement("li");
    item.textContent = "Not detected";
    experienceList.appendChild(item);
  }
}

function renderEducation(education) {
  if (education.levels.length > 0) {
    educationText.textContent = education.levels.join(", ");
  } else if (education.degree_mentioned) {
    educationText.textContent = "A degree is mentioned, but no specific level was detected.";
  } else {
    educationText.textContent = "Not detected";
  }
}

button.addEventListener("click", async () => {
  result.hidden = true;
  const text = textArea.value.trim();

  if (!text) {
    showMessage("Please paste a job description.", "error");
    return;
  }

  button.disabled = true;
  showMessage("Analyzing the job description...", "info");

  try {
    const response = await fetch("/api/job/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });
    const data = await response.json();

    if (!response.ok) {
      const detail = typeof data.detail === "string" ? data.detail : "Something went wrong.";
      showMessage(detail, "error");
      return;
    }

    const s = data.skills;
    showMessage("Job analyzed.", "success");
    summary.textContent = data.characters + " characters analysed.";
    noHeadings.hidden = s.has_requirement_sections;
    fillChips("required-list", s.required, "None detected");
    fillChips("preferred-list", s.preferred, "None detected");
    fillChips("responsibilities-list", s.in_responsibilities, "None detected");
    fillChips("mentioned-list", s.mentioned, "None");
    renderExperience(data.experience);
    renderEducation(data.education);
    result.hidden = false;
  } catch (error) {
    showMessage("Could not reach the server. Check your connection and try again.", "error");
  } finally {
    button.disabled = false;
  }
});