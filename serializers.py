# serializer for the api

# imports
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the user object
    """
    class Meta:
        model = User  # noqa
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'password'
        ]


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the issue object
    """

    class Meta:
        model = Issue  # noqa
        fields = [
            'title',
            'desc',
            'tag',
            'priority',
            'project_id',
            'status',
            'author_user_id',
            'assignee_user_id',
            'created_time',
        ]


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the project object
    """

    class Meta:
        model = Project  # noqa
        fields = [
            'project_id',
            'title',
            'description',
            'type',
            'author_user_id',
        ]


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the contributor object
    """

    class Meta:
        model = Contributor  # noqa
        fields = [
            'user_id',
            'project_id',
            'permission',
            'role',
        ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the comment object
    """

    class Meta:
        model = Comment  # noqa
        fields = [
            'comment_id',
            'description',
            'author_user_id',
            'issue_id',
            'created_time',
        ]