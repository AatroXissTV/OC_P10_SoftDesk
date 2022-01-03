from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local imports
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer
from .permissions import IsProjectAuthor


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):

        """
        Return the list of projects to which the user contributes.
        """

        return Project.objects.filter(contributors__user_id=self.request.user)

    def perform_create(self, serializer):

        """
        Set the logged in user as the author of the project.
        when a new project is created, it creates a contributor instance
        for this project with the logged in user.
        """

        new_project = serializer.save(author_user_id=self.request.user.id)
        author = Contributor(project=new_project,
                             user=self.request.user,
                             role='author')
        author.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContributorViewSet(viewsets.ModelViewSet):

    serializer_class = ContributorSerializer

    def create(self, request, project_pk=None):

        """"
        Create a new contributor for a specific project.
        """

        get_object_or_404(Project, pk=project_pk)
        data = request.data.copy()

        if 'project' not in data:
            data.update({'project': str(project_pk)})
        serializer = ContributorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        """
        Return the list of contributors associated to a specific project.
        """

        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])


class IssueViewSet(viewsets.ModelViewSet):
    """
    Return the list of issues associated to a specific project.
    Users that are authors of the issue can edit and delete it.
    """

    serializer_class = IssueSerializer

    def get_queryset(self):

        """
        Return the list of issues associated to a specific project
        """

        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, project_pk=None):

        """
        Create a new issue for a specific project.
        """

        get_object_or_404(Project, pk=project_pk)
        serializer = IssueSerializer(
            context={'request': request},
            data=request.data)
        if serializer.is_valid():
            serializer.save(
                author_user_id=request.user,
                project_id=Project.objects.get(pk=project_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):

        """
        Return the list of comments associated to a specific issue.
        """

        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def create(self, request, pk=None, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(
            pk=issue_pk,
            project=project_pk
        ).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment = get_object_or_404(Comment, pk=pk, issue=issue_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author_user_id=self.request.user,
                issue_id=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
