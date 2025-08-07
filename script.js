// Mock fallback data
const mockData = {
  results: [
    {
      question: "What is the capital of France?",
      correct_answer: "Paris",
      incorrect_answers: ["Berlin", "Madrid", "London"]
    }
  ]
};

// Get trivia data safely
async function getTriviaData() {
  try {
    const response = await fetch("https://opentdb.com/api.php?amount=1&type=multiple");

    if (!response.ok) {
      throw new Error(`API Error ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.warn("API failed, using mock data:", error.message);
    return mockData; // fallback
  }
}

// DOM elements
const question = document.getElementById("question");
const choice1 = document.getElementById("choice-1");
const choice2 = document.getElementById("choice-2");
const choice3 = document.getElementById("choice-3");
const choice4 = document.getElementById("choice-4");

getTriviaData().then(data => {
  const result = data.results[0];
  question.innerHTML = result.question;

  // Shuffle answers
  const answers = [result.correct_answer, ...result.incorrect_answers]
    .sort(() => Math.random() - 0.5);

  // Set text
  choice1.textContent = answers[0];
  choice2.textContent = answers[1];
  choice3.textContent = answers[2];
  choice4.textContent = answers[3];
});
