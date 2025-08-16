function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

/** Gathers data from server to handle current
 * question and display new trivia question and answers.
 */
function get_new_data(answer) {
  fetch("/get/new/data", { // TODO: create server side endpoint with logic
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      user_answer: document.getElementById(answer).textContent,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      handle_new_data(data); // TODO: write function
    })
    .catch((error) => {
      console.error("There was an error fetching new trivia data: ", error);
    });
}

function checkAnswer(answer) {
  let is_correct = false;
  let user_answer = document.getElementById(answer).textContent;
  let correct_answer = null;

  fetch("/get/correct/answer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      question: document.getElementById("question").textContent,
    }),
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

      if (is_correct) {
        document.getElementById(answer).style.color = "green";
      } else {
        document.getElementById(answer).style.color = "red";
      }

      setTimeout(() => {
        document.getElementById(answer).style.color = "white";

        // Fetch new question inside the timeout so color reset happens first
        fetch("/get/trivia/data")
          .then((response) => response.json())
          .then((data) => {
            let answers = [];
            document.getElementById("question").textContent =
              data["results"][0]["question"];
            answers.push(data["results"][0]["correct_answer"]);
            for (let i = 0; i < 3; i++) {
              answers.push(data["results"][0]["incorrect_answers"][i]);
            }

            answers = answers.sort(() => Math.random() - 0.5);
            for (let i = 0; i < answers.length; i++) {
              document.getElementById("choice-" + (i + 1)).textContent =
                answers[i];
            }
          })
          .catch((error) =>
            console.error("There was an error fetching data: ", error)
          );
      }, 2000);
    })
    .catch((error) => {
      console.error("There was an error fetching correct answer: ", error);
    });
}
