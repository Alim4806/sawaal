document.addEventListener("DOMContentLoaded", function () {
    let currentQuestionIndex = 0;
    let questions = [];
    let userAnswers = [];
    let timeLeft = 30; // Set timer duration in seconds
    let timerElement = document.getElementById("timer"); // Get timer element
    let countdown;

    // ✅ Check if all required elements exist
    const questionNumberElement = document.getElementById("question-number");
    const questionTextElement = document.getElementById("question-text");
    const optionButtons = document.querySelectorAll(".option-btn");

    if (!questionNumberElement || !questionTextElement || optionButtons.length === 0) {
        console.error("Error: Required elements are missing in the HTML.");
        return;
    }

    // ✅ Category mappings (Frontend → Backend format)
    const categoryMappings = {
        "general": "General Knowledge",
        "science": "Science & Technology",
        "history": "History & Geography",
        "math": "Mathematics & Logic",
        "entertainment": "Entertainment",
        "sports": "Sports"
    };

    function getCategoryFromURL() {
        const pathParts = window.location.pathname.split('/');
        let category = pathParts[pathParts.length - 1];
        return decodeURIComponent(category);
    }

    async function fetchQuestions() {
        try {
            let category = getCategoryFromURL();
            category = categoryMappings[category.toLowerCase()] || category;
            console.log("Mapped category:", category);

            const response = await fetch(`/api/quiz?category=${encodeURIComponent(category)}`);
            const data = await response.json();

            if (data.error) {
                console.error("Error fetching questions:", data.error);
                return;
            }

            questions = data.questions;
            if (!questions || questions.length === 0) {
                console.error("No questions available for this category.");
                return;
            }

            console.log("Questions fetched successfully:", questions);
            displayQuestion(); 
            startTimer();
        } catch (error) {
            console.error("Error fetching questions:", error);
        }
    }

    function displayQuestion() {
        if (currentQuestionIndex >= questions.length) {
            localStorage.setItem("userAnswers", JSON.stringify(userAnswers));
            window.location.href = "/result";
            return;
        }

        let questionData = questions[currentQuestionIndex];

        // ✅ Ensure elements exist before updating
        if (questionNumberElement) {
            questionNumberElement.textContent = `Question ${currentQuestionIndex + 1}`;
        }

        if (questionTextElement) {
            questionTextElement.innerHTML = htmlDecode(questionData.text);
        }

        let options = [
            htmlDecode(questionData.option_a),
            htmlDecode(questionData.option_b),
            htmlDecode(questionData.option_c),
            htmlDecode(questionData.option_d)
        ];

        optionButtons.forEach((btn, index) => {
            if (btn) {
                btn.textContent = options[index];
                btn.onclick = () => selectAnswer(options[index], questionData.correct_answer);
            }
        });

        timeLeft = 30; 
        updateTimerDisplay();
    }

    function selectAnswer(selected, correct) {
        userAnswers.push({ selected, correct });
        nextQuestion();
    }

    function nextQuestion() {
        clearInterval(countdown);
        currentQuestionIndex++;
        displayQuestion();
        startTimer();
    }

    function startTimer() {
        clearInterval(countdown);
        timeLeft = 30; 
        updateTimerDisplay();

        countdown = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            if (timeLeft <= 0) {
                clearInterval(countdown);
                nextQuestion();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        if (timerElement) {
            timerElement.textContent = `Time left: ${timeLeft}s`;
        }
    }

    function htmlDecode(input) {
        let doc = new DOMParser().parseFromString(input, "text/html");
        return doc.documentElement.textContent;
    }

    fetchQuestions();
});
