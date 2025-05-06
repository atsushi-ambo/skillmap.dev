// Quiz interaction functionality
document.addEventListener("DOMContentLoaded", () => {
  // Initialize all quiz options
  document.querySelectorAll(".quiz-options").forEach((list) => {
    list.querySelectorAll("li").forEach((li) => {
      li.addEventListener("click", (e) => {
        // Prevent multiple clicks
        if (li.classList.contains("clicked")) return;
        
        const isCorrect = li.dataset.correct === "true";
        
        // Add appropriate class based on answer
        li.classList.add(isCorrect ? "correct" : "incorrect");
        li.classList.add("clicked");
        
        // Disable further clicks on all options
        list.querySelectorAll("li").forEach((option) => {
          option.style.pointerEvents = "none";
          
          // Show correct answer if user clicked wrong one
          if (option.dataset.correct === "true" && !isCorrect) {
            option.classList.add("correct");
          }
        });
        
        // Prevent event bubbling
        e.stopPropagation();
      });
    });
  });
});
