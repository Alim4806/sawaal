document.addEventListener("DOMContentLoaded", function () {
    let userAnswers = JSON.parse(localStorage.getItem("userAnswers")) || [];
    let totalQuestions = userAnswers.length;
    let correctAnswers = 0;

    userAnswers.forEach(answer => {
        if (answer.selected === answer.correct) {
            correctAnswers++;
        }
    });

    let incorrectAnswers = totalQuestions - correctAnswers;
    let score = `${correctAnswers} / ${totalQuestions}`;

    document.getElementById("score").innerText = `Your Score: ${score}`;
    document.getElementById("correct-answers").innerText = `Correct Answers: ${correctAnswers}`;
    document.getElementById("incorrect-answers").innerText = `Incorrect Answers: ${incorrectAnswers}`;

    // Add event listeners for buttons
    document.getElementById("try-again-btn").addEventListener("click", function () {
        window.location.href = "quiz.html"; // Restart quiz
    });

    document.getElementById("choose-another-quiz-btn").addEventListener("click", function () {
        window.location.href = "categories.html"; // Back to categories
    });
});

