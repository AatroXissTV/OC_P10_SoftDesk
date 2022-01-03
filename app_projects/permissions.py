from rest_framework import permissions

from app_projects.models import Project


class IsProjectAuthor(permissions.BasePermission):
    """
    Checking if the user is the author of the project.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsProjectContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        ctr_projects = Project.objects.filter(contributors__user=request.user)

        if project in ctr_projects:
            project = Project.objects.get(id=view.kwargs['project_pk'])
            if request.method in permissions.SAFE_METHODS:
                return True
            return project.author_user == request.user
        return False

    def has_object_permission(self, request, view, obj):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == project.author_user


class IsIssueAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        ctr_projects = Project.objects.filter(contributors__user=request.user)

        if project in ctr_projects:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author_user


class IsCommentAuthor(permissions.BasePermission):
    pass
