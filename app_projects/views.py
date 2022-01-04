from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local imports
from .models import (
    Project,
    Contributor,
    Issue,
    Comment
)

from .serializers import (
    CommentSerializer,
    IssueSerializer,
    ProjectSerializer,
    ContributorSerializer
)

from .permissions import (
    IsCommentAuthor,
    IsProjectAuthor,
    IsProjectContributor,
    IsIssueAuthor
)


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        """
        Overriding the get_queryset method to return the projects
        that the user is a contributor of.
        """
        return Project.objects.filter(contributors__user_id=self.request.user)

    def perform_create(self, serializer):
        """
        Overriding the perform_create method to add the author to the
        project's contributors.
        """

        serializer.save(author_user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        """
        Return all the contributors of the project.
        """
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, project_pk=None):
        """
        Overriding the create method to add the user as a contributor
        to the project.
        """

        data = request.data.copy()
        contributors_list = []

        for object in Contributor.objects.filter(project_id=project_pk):
            contributors_list.append(object.user_id)

        # check if the user is already a contributor
        if int(data['user']) in contributors_list:
            return Response(
                {'error': 'User is already a contributor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # add the user as a contributor
            data['project'] = project_pk
            data['role'] = 'contributor'
            serializer = ContributorSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {'message': 'User added as contributor'},
                status=status.HTTP_201_CREATED
            )


class IssueViewSet(viewsets.ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueAuthor]

    def get_queryset(self):
        """
        Overriding the get_queryset method to return the issues
        of the project.
        """
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, project_pk=None):
        """
        Overriding the create method to create an issue.
        """

        data = request.data.copy()

        # check if the issue already exists
        if Issue.objects.filter(title=data['title']).exists():
            return Response(
                {'error': 'Issue already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data['author_user'] = self.request.user.pk
        data['project'] = project_pk

        if 'assignee_user' not in data:
            data['assignee_user'] = request.user.pk

        serialized_data = IssueSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(
            {'message': 'Issue created'},
            status=status.HTTP_201_CREATED
        )


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def create(self, request, project_pk=None, issue_pk=None):

        data = request.data.copy()
        data['author_user'] = self.request.user.pk
        data['issue'] = issue_pk

        serialized_data = CommentSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(
            {'message': 'Comment created'},
            status=status.HTTP_201_CREATED
        )
