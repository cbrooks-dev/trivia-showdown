function checkAnswer(answer) {
  let is_correct = false;
  let user_answer = document.getElementById(answer).textContent;
  let correct_answer = null;

  fetch("/get/correct/answer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({question: document.getElementById('question')}),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      try {
        correct_answer = data["correct_answer"];
      } catch (error) {
        correct_answer = null;
      }
    })
    .catch((error) => {
      console.error("There was an error fetching correct answer: ", error);
    });

  if (user_answer == correct_answer) {
    // Check if correct answer chosen
    is_correct = true;
  }

  if (is_correct) {
    // Change to corresponding text color
    document.getElementById(answer).style.color = "green";
  } else {
    document.getElementById(answer).style.color = "red";
  }

  setTimeout(() => {}, 2000); // Set timeout and then revert to original color
  document.getElementById(answer).style.color = "white";

  fetch("/get/trivia/data") // Gather new trivia data
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let answers = [];
      document.getElementById("question").textContent =
        data["results"][0]["question"];
      answers.push(data["results"][0]["correct_answer"]);
      for (let i = 0; i < 3; i++) {
        answers.push(data["results"][0]["incorrect_answers"][i]);
      }

      // Randomly assign answer choices to html buttons
      answers = answers.sort(() => Math.random() - 0.5);
      for (let i = 0; i < answers.length; i++) {
        document.getElementById("choice-" + (i + 1)).textContent = answers[i];
      }
    })
    .catch((error) => {
      console.error("There was an error fetching data: ", error);
    });
}
