import openai
import os, requests
from django.conf import settings
from django.utils.translation import gettext as _
from .models import AIRequest

OPENAI_API_KEY = settings.OPENAI_API_KEY
DEEPSEEK_BASE_URL = settings.DEEPSEEK_BASE_URL

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=DEEPSEEK_BASE_URL)

def generate_questions(teacher_id, subject, difficulty, num_questions, num_answers, language="en", feedback=None):
    prompt = f"Generate {num_questions} multiple-choice questions for {subject} with {num_answers} answer choices each. The difficulty level should be {difficulty}."

    print(f"Generated Prompt: {prompt}")  # Debugging

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "You are a helpful assistant"},
                      {"role": "user", "content": prompt}],
            stream=False
        )

        print("DeepSeek Response:", response)  # Debugging

        ai_response = response.choices[0].message.content

        # Save AI request history
        AIRequest.objects.create(
            teacher_id=teacher_id,
            subject=subject,
            difficulty=difficulty,
            num_questions=num_questions,
            num_answers=num_answers,
            previous_prompt=prompt,
            previous_response={"response": ai_response},
            feedback=feedback,
            language=language
        )

        return {"questions": ai_response}

    except openai.APIError as e:
        print("DeepSeek API Error:", str(e))  # Debugging
        return {"error": _("DeepSeek API request failed"), "details": str(e)}