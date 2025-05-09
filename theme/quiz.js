// Quiz interaction functionality with explanations
document.addEventListener("DOMContentLoaded", () => {
  // Mark function to handle quiz answer feedback
  const mark = (li, ok) => {
    li.classList.add(ok ? "correct" : "incorrect");
    if (!li.querySelector(".result-label")) {
      li.insertAdjacentHTML("beforeend",
        `<span class="result-label">${ok ? "✔ 正解" : "✖ 不正解"}</span>`
      );
      const exp = li.dataset.explain || "";
      if (exp) li.insertAdjacentHTML("beforeend",
        `<div class="explain">${exp}</div>`
      );
    }
  };

  // Initialize all quiz options
  document.querySelectorAll(".quiz-options").forEach((list) => {
    list.querySelectorAll("li").forEach((li) => {
      li.addEventListener("click", (e) => {
        const li = e.currentTarget; // Use the element that was actually clicked
        
        // Guard: highlight li's missing dataset
        if (!li.hasAttribute("data-correct")) {
          console.warn("quiz-options > li missing data-correct attribute:", li);
          return;
        }
        
        // Prevent multiple clicks
        if (li.classList.contains("clicked")) return;
        
        const isCorrect = li.dataset.correct === "true";
        
        // Mark the clicked answer
        mark(li, isCorrect);
        
        // Mark all other options as disabled
        list.querySelectorAll("li").forEach((option) => {
          option.style.pointerEvents = "none";
          
          // Show correct answer with explanation if user clicked wrong one
          if (option.dataset.correct === "true" && !isCorrect) {
            mark(option, true);
          }
        });
      });
    });
  });
        // Prevent event bubbling
        e.stopPropagation();
      });
    });
  });
});
