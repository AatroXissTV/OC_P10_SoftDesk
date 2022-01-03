from rest_framework import permissions


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
    pass


class IsIssueAuthor(permissions.BasePermission):
    pass


class IsCommentAuthor(permissions.BasePermission):
    pass
