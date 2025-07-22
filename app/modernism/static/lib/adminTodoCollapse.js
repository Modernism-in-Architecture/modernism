function initializeToDoCollapse() {
  document.querySelectorAll(".country-group, .city-group").forEach((group) => {
    group.classList.remove("open");
  });

  document.querySelectorAll(".toggle-section").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const parent = toggle.parentElement;
      parent.classList.toggle("open");
    });
  });
}