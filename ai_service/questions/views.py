from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils.translation import gettext as _
from .utils import generate_questions

@api_view(['POST'])
def generate_questions_api(request):
    teacher_id = request.data.get('teacher_id')
    subject = request.data.get('subject')
    difficulty = request.data.get('difficulty')
    num_questions = int(request.data.get('num_questions', 5))
    num_answers = int(request.data.get('num_answers', 4))
    language = request.headers.get('Accept-Language', 'en')
    feedback = request.data.get('feedback', None)

    if not teacher_id or not subject or not difficulty:
        return Response({"error": _("Teacher ID, Subject, and Difficulty are required")}, status=400)

    # Step 1: Generate AI-based questions
    questions_data = generate_questions(teacher_id, subject, difficulty, num_questions, num_answers, language, feedback)

    if "error" in questions_data:
        return Response({"error": questions_data["error"]}, status=500)

    return Response({
        "message": _("Questions generated successfully. Please review before saving."),
        "questions": questions_data["questions"]
    }, status=status.HTTP_200_OK)