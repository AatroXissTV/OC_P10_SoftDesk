from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local imports
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsProjectAuthor, IsProjectContributor


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

        serializer.is_valid(raise_exception=True)
        new_project = serializer.save(
            author_user_id=self.request.user.id
        )

        # add the user as a contributor
        author = Contributor.objects.create(
            user=self.request.user,
            project=new_project,
            role='author'
        )
        author.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        # check permissions
        request.is_valid(raise_exception=True)

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
            contributor = Contributor.objects.create(
                user_id=data['user'],
                project_id=project_pk,
                role=data['role'],
            )
            contributor.save()

            return Response(
                {'message': 'User added as contributor'},
                status=status.HTTP_201_CREATED
            )


class IssueViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
