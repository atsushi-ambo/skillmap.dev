// Quiz interaction functionality with explanations
document.addEventListener("DOMContentLoaded", () => {
  // Initialize all quiz options
  document.querySelectorAll(".quiz-options").forEach((list) => {
    list.querySelectorAll("li").forEach((li) => {
      li.addEventListener("click", (e) => {
        // Prevent multiple clicks
        if (li.classList.contains("clicked")) return;
        
        const isCorrect = li.dataset.correct === "true";
        const explanation = li.dataset.explain || "";
        
        // Add appropriate class based on answer
        li.classList.add(isCorrect ? "correct" : "incorrect");
        li.classList.add("clicked");
        
        // Add explanation if exists
        if (explanation) {
          const explainEl = document.createElement("div");
          explainEl.className = "explanation";
          explainEl.textContent = explanation;
          li.appendChild(explainEl);
        }
        
        // Disable further clicks on all options and show explanations
        list.querySelectorAll("li").forEach((option) => {
          option.style.pointerEvents = "none";
          
          // Show correct answer with explanation if user clicked wrong one
          if (option.dataset.correct === "true") {
            if (!isCorrect) {
              option.classList.add("correct");
              if (option.dataset.explain) {
                const correctExplain = document.createElement("div");
                correctExplain.className = "explanation";
                correctExplain.textContent = option.dataset.explain;
                option.appendChild(correctExplain);
              }
            }
          }
        });
        
        // Prevent event bubbling
        e.stopPropagation();
      });
    });
  });
});
