function getTriviaData() {
    fetch("https://opentdb.com/api.php?amount=10")
        .then(response => {
            response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error("Error fetching api: ", error);
        });
}

const question = document.getElementById("question");
const choice1 = document.getElementById("choice-1");