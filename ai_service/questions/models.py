from django.db import models

class AIRequest(models.Model):
    teacher_id = models.IntegerField()
    subject = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    num_questions = models.IntegerField()
    num_answers = models.IntegerField()
    previous_prompt = models.TextField()
    previous_response = models.JSONField()
    feedback = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.language}) - {self.created_at}"
