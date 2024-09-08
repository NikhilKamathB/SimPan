from markdown import markdown
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from comfychat.validators import ChatAPIResponse
from comfychat.decorators import post_chat_view_handler

from comfychat import AGENT



def index(request):
    return render(request, "comfychat/comfychat.html")

@post_chat_view_handler
def chat(request):
    query = request.POST.get("chat-query")
    if not query:
        raise BadRequest("You have not provided a query.")
    workspace_id = request.POST.get("workspace-id")
    agent_response = AGENT.invoke({"question": query})
    response_raw = agent_response.get("output", "Sorry! I was unable to generate any respone. Contact Nikhil.")
    response_html = markdown(response_raw)

    
    uploaded_files = []
    return JsonResponse(
        ChatAPIResponse(success=True, message="Success", description=response_html, data={
            "uploaded_files": uploaded_files
        }).model_dump(),
        status=status.HTTP_200_OK
    )