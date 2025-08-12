from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    answered_trivia_questions = models.ManyToManyField(
        "TriviaQuestion", blank=True, related_name="answered_by"
    )

    def save(self, *args, **kwargs):
        # Automatically hash the password if it's not already hashed
        if not self.password.startswith("pbkdf2_"):  # crude check
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class TriviaQuestion(models.Model):
    response_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trivia Question #{self.id}"


class TriviaResults(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    type = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100)
    question = models.CharField(max_length=1000)
    correct_answer = models.CharField(max_length=1000)
    incorrect_answers = models.JSONField()
    trivia_question = models.OneToOneField(
        TriviaQuestion, on_delete=models.CASCADE, related_name="results"
    )

    def __str__(self):
        return f"{self.category} - {self.question[:50]}..."
