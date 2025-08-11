function checkAnswer(answer) {
  is_correct = false;
  answer = document.getElementById(answer);
  fetch("/get/trivia/data")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data; // TODO: handle response data
    })
    .catch((error) => {
      console.error("There was an error fetching data: ", error);
    });
}
