import requests
from .models import *


def get_trivia_data() -> dict: # TODO: clean up db access and add user db persistence
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
        data = request.json()
        tq = TriviaQuestion(response_code=data["response_code"])
        tq.save()
        results = data["results"]
        tr = TriviaResults(
            type=results[0]["type"],
            difficulty=results[0]["difficulty"],
            category=results[0]["category"],
            question=results[0]["question"],
            correct_answer=results[0]["correct_answer"],
            incorrect_answers=results[0]["incorrect_answers"],
            trivia_question=tq,
        )
        tr.save()
        return data
    else:
        print(f"Bad request: {request.status_code}")
        return mock_trivia_data



def get_correct_answer(question_text: str) -> dict:
    try:
        result = TriviaResults.objects.get(question=question_text)
        return {'question': result.question, 'correct_answer': result.correct_answer}
    except TriviaResults.DoesNotExist:
        return {'error': 'Question not found'}
