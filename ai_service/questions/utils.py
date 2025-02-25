import json
from django.conf import settings
from django.utils.translation import gettext as _
import google.generativeai as genai
from .models import AIRequest

# Load API key
GOOGLE_GEMINI_API_KEY = settings.GOOGLE_GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

def generate_questions(teacher_id, subject, difficulty, num_questions, num_answers, language="en", feedback=None):
    """
    Generate AI-based multiple-choice questions using Google Gemini API.
    Ensures structured JSON output in the specified language.
    """
    # Map language codes to full language names
    language_map = {
        'en': 'English',
        'ru': 'Russian',
        'az': 'Azerbaijani'
    }
    
    language_name = language_map.get(language, 'English')
    
    prompt = f"""
    You are an AI that generates structured JSON-formatted multiple-choice questions.
    Generate all questions and answers in {language_name} language only.
    Do not return explanations or extra text. Return only valid JSON.

    Generate {num_questions} multiple-choice questions for {subject}.
    - Each question must have {num_answers} answer choices.
    - The difficulty level should be {difficulty}.
    - Avoid numerical calculations.
    - ALL TEXT MUST BE IN {language_name.upper()} LANGUAGE ONLY.
    
    **FORMAT:**
    {{
        "questions": [
            {{
                "text": "Question text here in {language_name}",
                "default_score": "1.00",
                "answers": [
                    {{"text": "Answer 1 in {language_name}", "is_correct": false}},
                    {{"text": "Answer 2 in {language_name}", "is_correct": false}},
                    {{"text": "Answer 3 in {language_name}", "is_correct": true}},
                    {{"text": "Answer 4 in {language_name}", "is_correct": false}}
                ]
            }},
            ...
        ]
    }}
    
    Make sure to output only valid JSON without any extra text.
    """

    if feedback:
        prompt += f" The teacher provided feedback: '{feedback}'. Improve based on this feedback."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Extract text response
        response_text = response.text.strip()

        # Attempt to extract only JSON content
        response_text = response_text.strip("```json").strip("```").strip()

        # Ensure response is correctly formatted
        try:
            structured_response = json.loads(response_text)
        except json.JSONDecodeError:
            print("Error: Gemini response is not valid JSON. Logging response for debugging.")
            structured_response = None

        if not structured_response or "questions" not in structured_response:
            return {
                "error": _("Invalid JSON response from Gemini"),
                "raw_output": response_text
            }

        # Save AI request history
        AIRequest.objects.create(
            teacher_id=teacher_id,
            subject=subject,
            difficulty=difficulty,
            num_questions=num_questions,
            num_answers=num_answers,
            previous_prompt=prompt,
            previous_response=structured_response,
            feedback=feedback,
            language=language
        )

        return structured_response  # Returns properly formatted JSON

    except Exception as e:
        print("Gemini API Error:", str(e))  # Debugging
        return {"error": _("Gemini API request failed"), "details": str(e)}