// Task list persistence
(() => {
  // Persist task-list checkboxes
  const STORAGE_KEY = "skillmap-checklist";
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");

  // Mark saved states
  document.querySelectorAll("ul.task-list input[type=checkbox]").forEach((cb, i) => {
    cb.checked = saved[i] ?? cb.checked;
    cb.addEventListener("change", () => {
      saved[i] = cb.checked;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
    });
  });
})();
