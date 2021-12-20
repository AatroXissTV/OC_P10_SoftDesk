from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        serializer = ProjectSerializer(
            context={'request': request},
            data=request.data)
        if serializer.is_valid():
            print(request.user)
            serializer.save(
                title=request.data['title'],
                description=request.data['description'],
                type=request.data['type'],
                author_user_id=request.user
            )
            contributor = Contributor(
                user_id=request.user,
                project_id=serializer.instance,
                role='author'
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        issues = Issue.objects.filter(project_id=pk)
        contributors = Contributor.objects.filter(project_id=pk)
        self.check_object_permissions(request, project)
        project.delete()
        for issue in issues:
            comments = Comment.objects.filter(issue=issue.pk)
            for comment in comments:
                comment.delete()
        for contributor in contributors:
            contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewSet(viewsets.ModelViewSet):

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        data = request.data.copy()
        if 'project' not in data:
            data.update({'project': str(project_pk)})
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(viewsets.ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
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

    def create(self, request, pk=None, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(
            pk=issue_pk,
            project=project_pk
        ).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment = get_object_or_404(Comment, pk=pk, issue=issue_pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author_user_id=self.request.user,
                issue_id=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
