import requests
from .models import *
import json
import html
import random


def home() -> dict:
    """Gathers first question and choices to display upon rendering home html."""

    return get_extracted_data()


def get_new_data(request) -> dict:
    """Returns new question data to display on UI and checks for correct answer of current question."""

    data = json.loads(request.body)

    question = data.get("question")
    if not question:
        return {"error": "Question was not provided by client request."}

    user_answer = data.get("user_answer")
    if not user_answer:
        return {"error": "User Answer was not provided by client request."}

    trivia_data = get_extracted_data()

    correct_answer = get_correct_answer(question)
    if correct_answer is None:
        return {"error": "Question not found in the database."}

    user_correct = is_user_correct(user_answer, correct_answer)

    # popup_data = get_popup_data() TODO: write function

    new_data = trivia_data
    new_data["user_correct"] = user_correct
    # new_data["popup_data"] = popup_data TODO: uncomment

    return new_data


def is_user_correct(user_answer, correct_answer) -> bool:
    """Checks if user answer matches the question's correct answer."""

    try:
        return str(user_answer).lower() == str(correct_answer).lower()
    except TypeError as te:
        return False


def get_extracted_data() -> dict:
    """Returns only data that will be displayed on UI."""

    data = get_trivia_data()["results"][0]

    question = data["question"]

    choices = []
    choices.append(data["correct_answer"])

    for answer in data["incorrect_answers"]:
        choices.append(answer)
    random.shuffle(choices)

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
    
    trivia_question = TriviaQuestion(response_code=mock_trivia_data.get("response_code"))
    trivia_question.save()
    r = mock_trivia_data["results"][0]
    trivia_results = TriviaResults(
        type=r["type"],
        difficulty=r["difficulty"],
        category=r["category"],
        question=r["question"],
        correct_answer=r["correct_answer"],
        incorrect_answers=r["incorrect_answers"],
        trivia_question=trivia_question,
    )
    trivia_results.save()

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


def get_correct_answer(question_text) -> str:
    """Gets the correct answer of current question from TriviaResults objects."""

    results = TriviaResults.objects.filter(question=str.strip(question_text))
    if results.exists():
        return results.first().correct_answer
    else:
        return None
    