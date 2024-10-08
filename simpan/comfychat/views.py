import json
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.shortcuts import render, redirect
from db.models import Workspace
from services.validators import BaseFileStruct


def index(request):
    if not request.user.is_authenticated:
        login_url = reverse("account:login")
        return redirect(f"{login_url}?{urlencode({'next': reverse("comfychat:comfychat")})}")
    workspace_dict = {}
    workspaces = Workspace.objects.prefetch_related("workspace_files").filter(user=request.user).order_by("-updated_at")
    if workspaces.count() == 0:
        workspace = Workspace.objects.create(user=request.user)
    for workspace in workspaces:
        context = {}
        context["workspace"] = str(workspace.id)
        context["workspace_name"] = workspace.name
        context["workspace_files"] = [
            BaseFileStruct(id=str(f.id), name=f.file.name, url=f.file.url, type=f.file.name.split(".")[-1].lower()).model_dump(mode="json")
            for f in workspace.workspace_files.all()
        ]
        context["workspace_chat"] = workspace.conversation
        context["workspace_created_at"] = timezone.localtime(workspace.created_at).strftime("%d %B %Y %H:%M")
        context["workspace_updated_at"] = timezone.localtime(workspace.updated_at).strftime("%d %B %Y %H:%M")
        workspace_dict[str(workspace.id)] = context
    context = workspace_dict
    return render(request, "comfychat/comfychat.html", {
        "context": json.dumps(context)
    })