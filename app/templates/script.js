function checkAnswer(answer) {
  let is_correct = false;
  let user_answer = document.getElementById(answer);
  let correct_answer = null;

  fetch("/get/correct/answer") // Get current correct answer
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      correct_answer = data["correct_answer"];
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
      // TODO: randomly assign answer choices to html buttons
    })
    .catch((error) => {
      console.error("There was an error fetching data: ", error);
    });
}
