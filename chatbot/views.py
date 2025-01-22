from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from .models import ChatLog, UserPreference
from .ai_backend import process_query
from .pdf_processor import summarize_pdf
from .web_scraper import fetch_web_info

@login_required
def chatbot_view(request):
    """Render the main chatbot interface."""
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)
    context = {
        'default_role': user_pref.default_role,
        'theme': user_pref.theme
    }
    return render(request, 'chatbot/chatbot.html', context)

@login_required
@csrf_exempt
def chat_endpoint(request):
    """Handle chat interactions."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        query = data.get('query')
        role = data.get('role', 'student')
        
        if not query:
            return JsonResponse({'error': 'Query is required'}, status=400)

        # Process the query through AI backend
        response = process_query(query, role, request.user)
        
        # Log the interaction
        ChatLog.objects.create(
            user=request.user,
            role=role,
            query=query,
            response=response
        )
        
        return JsonResponse({'response': response})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
def summarize_endpoint(request):
    """Handle PDF summarization requests."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    try:
        pdf_file = request.FILES['file']
        summary = summarize_pdf(pdf_file)
        return JsonResponse({'summary': summary})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)