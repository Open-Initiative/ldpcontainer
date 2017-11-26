from django.contrib.sites.models import get_current_site
from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from oi.helpers import OI_READ, OI_ANSWER, OI_BID, OI_MANAGE, OI_WRITE, OI_ALL_PERMS, jsonld_array
from oi.projects.models import Project, Spec, OINeedsPrjPerms, Release

#TODO: handle permissions
class LDPContainer(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LDPContainer, self).dispatch(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Accept-Post"] = "application/ld+json"
        return response
    def post(self, request, *args, **kwargs):
        response = HttpResponse()
        return response
    def get(self, request, id):
        """Return jsonLd object"""
        project = get_object_or_404(Project, id=id)
        
        response = render_to_response("ldp/project.json", {
            "project": project,
            "current_site": get_current_site(request),
            "tasks": jsonld_array(request, project.tasks, "/project/ldpcontainer/"),
            "descendants": jsonld_array(request, project.descendants, "/project/ldpcontainer/"),
            "messages": jsonld_array(request, project.message_set, "/message/ldpcontainer/"),
            "specs" : jsonld_array(request, project.spec_set, "/prjmgt/ldpcontainer/%s/specs/"%project.pk),
            "releases" : jsonld_array(request, project.release_set, "/prjmgt/ldpcontainer/%s/releases/"%project.pk, extra_fields=("name",)),
        })
        
        response = HttpResponse(serializers.ldpserialize("json", [project], extra_fields=()))
#        response["Content-Type"] = "application/ld+json"
        response["Access-Control-Allow-Origin"] = "*"
        return response
