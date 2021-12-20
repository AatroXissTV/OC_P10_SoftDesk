from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        return Project.objects.filter(contributor__user=self.request.user)

    def create(self, request):

        data = request.data.copy()
        data['author'] = request.user.id
        serialized = ProjectSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        project = serialized.save()

        contributor = Contributor.objects.create(
            user=request.user,
            project=project,
            role='author'
        )
        contributor.save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)


class ContributorViewSet(viewsets.ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewSet(viewsets.ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
