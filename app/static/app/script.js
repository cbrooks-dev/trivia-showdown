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

/**
 * Gathers data from server to handle current
 * question and display new trivia question and answers.
 * @param {*} answer the choice selected by user.
 */
function getNewData(answer) {
  fetch("/get/new/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      question: document.getElementById("question").textContent,
      user_answer: document.getElementById(answer).textContent,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let is_handled = handleNewData(data, answer);
      if (!is_handled) {
        console.error(data["error"]);
      }
    })
    .catch((error) => {
      console.error("There was an error fetching new trivia data: ", error);
    });
}

/**
 * Updates the UI with the new data.
 * @param {*} data the data to be handled.
 * @returns boolean value indicating whether data was able to be handled.
 */
function handleNewData(data, answer) {
  if (data["error"]) {
    return false; // Data was not handled
  }

  let question = data["question"];
  let choices = data["choices"];
  let userCorrect = data["user_correct"];
  // let popupData = data["popup_data"]; TODO: finish handling of popup data once server side sends data

  if (userCorrect) {
    document.getElementById(answer).style.color = "green";
  } else {
    document.getElementById(answer).style.color = "red";
  }

  setTimeout(() => {
    document.getElementById("question").textContent = question;
    document.getElementById(answer).style.color = "white";
    for (let i = 0; i < choices.length; i++) {
      document.getElementById("choice-" + (i + 1)).textContent = choices[i];
    }
  }, 2000);

  return true; // Data was handled
}

// function checkAnswer(answer) {
//   let is_correct = false;
//   let user_answer = document.getElementById(answer).textContent;
//   let correct_answer = null;

//   fetch("/get/correct/answer", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrftoken,
//     },
//     body: JSON.stringify({
//       question: document.getElementById("question").textContent,
//     }),
//   })
//     .then((response) => {
//       return response.json();
//     })
//     .then((data) => {
//       try {
//         correct_answer = data["correct_answer"];
//       } catch (error) {
//         correct_answer = null;
//       }

//       if (user_answer == correct_answer) {
//         // Check if correct answer chosen
//         is_correct = true;
//       }

//       if (is_correct) {
//         // Change to corresponding text color
//         document.getElementById(answer).style.color = "green";
//       } else {
//         document.getElementById(answer).style.color = "red";
//       }

//       if (is_correct) {
//         document.getElementById(answer).style.color = "green";
//       } else {
//         document.getElementById(answer).style.color = "red";
//       }

//       setTimeout(() => {
//         document.getElementById(answer).style.color = "white";

//         // Fetch new question inside the timeout so color reset happens first
//         fetch("/get/trivia/data")
//           .then((response) => response.json())
//           .then((data) => {
//             let answers = [];
//             document.getElementById("question").textContent =
//               data["results"][0]["question"];
//             answers.push(data["results"][0]["correct_answer"]);
//             for (let i = 0; i < 3; i++) {
//               answers.push(data["results"][0]["incorrect_answers"][i]);
//             }

//             answers = answers.sort(() => Math.random() - 0.5);
//             for (let i = 0; i < answers.length; i++) {
//               document.getElementById("choice-" + (i + 1)).textContent =
//                 answers[i];
//             }
//           })
//           .catch((error) =>
//             console.error("There was an error fetching data: ", error)
//           );
//       }, 2000);
//     })
//     .catch((error) => {
//       console.error("There was an error fetching correct answer: ", error);
//     });
// }
