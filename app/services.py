import requests
from .models import *
import json
import html


def home() -> dict:
    """Gathers first question and choices to display upon rendering home html."""

    data = get_trivia_data()["results"][0]
    question = data["question"]
    choices = []
    choices.append(data["correct_answer"])
    for answer in data["incorrect_answers"]:
        choices.append(answer)
    choices.sort()
    return {"question": question, "choices": choices}


def get_trivia_data() -> dict:
    """Gets a trivia question and relevant data from opentdb."""

    mock_trivia_data = {
        "response_code": 0,
        "results": [
            {
                "type": "multiple",
                "difficulty": "medium",
                "category": "Science &amp; Nature",
                "question": "The moons, Miranda, Ariel, Umbriel, Titania and Oberon orbit which planet?",
                "correct_answer": "Uranus",
                "incorrect_answers": ["Jupiter", "Venus", "Neptune"],
            }
        ],
    }

    try:
        request = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    except Exception as e:
        print(f"Could not get trivia data: {e}")
        return mock_trivia_data

    if request.ok:
        data = unescape_data(dict(request.json()))
        tq = TriviaQuestion(response_code=data["response_code"])
        tq.save()
        results = data["results"][0]
        tr = TriviaResults(
            type=results["type"],
            difficulty=results["difficulty"],
            category=results["category"],
            question=results["question"],
            correct_answer=results["correct_answer"],
            incorrect_answers=results["incorrect_answers"],
            trivia_question=tq,
        )
        tr.save()
        return data
    else:
        print(f"Bad request: {request.status_code}")
        return mock_trivia_data
    
    
def unescape_data(data: dict) -> dict:
    """Recursively unescapes HTML entities in all string values within a dictionary or list."""

    if isinstance(data, dict):
        return {k: unescape_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [unescape_data(item) for item in data]
    elif isinstance(data, str):
        return html.unescape(data)
    else:
        return data


def get_correct_answer(request) -> dict:
    """Gets the correct answer of current question from TriviaResults objects."""

    data = json.loads(request.body)
    question_text = data.get("question")
    if not question_text:
        return {"error": 'Missing "question" parameter'}

    try:
        result = TriviaResults.objects.get(question=question_text)
        return {"question": result.question, "correct_answer": result.correct_answer}
    except TriviaResults.DoesNotExist:
        return {"error": "Question not found"}
