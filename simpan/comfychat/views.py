import json
from django.shortcuts import render
from services.validators import BaseFileStruct
from db.models import Workspace, WorkspaceStorage


def index(request):
    workspace = request.session.get("workspace")
    if not workspace:
        workspace_obj = Workspace.objects.create()
    else:
        workspace_obj, _ = Workspace.objects.get_or_create(id=workspace)
    request.session["workspace"] = str(workspace_obj.id)
    workspace_files_obj = WorkspaceStorage.objects.filter(workspace=workspace_obj)
    workspace_files_obj_list = [
        BaseFileStruct(id=str(f.id), name=f.file.name, url=f.file.url, type=f.file.name.split(".")[-1].lower()).model_dump(mode="json")
        for f in workspace_files_obj
    ]
    context = {
        "workspace": str(workspace_obj.id),
        "workspace_files": json.dumps(workspace_files_obj_list)
    }
    return render(request, "comfychat/comfychat.html", context)