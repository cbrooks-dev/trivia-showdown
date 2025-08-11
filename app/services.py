import requests


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
        return request.json()
    else:
        print(f"Bad request: {request.status_code}")
        return mock_trivia_data
