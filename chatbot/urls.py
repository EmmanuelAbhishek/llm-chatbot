from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_view, name='chat_interface'),
    path('api/chat/', views.chat_endpoint, name='chat_endpoint'),
    path('api/summarize/', views.summarize_endpoint, name='summarize_endpoint'),
]