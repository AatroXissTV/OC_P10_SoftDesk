from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author_user_id', 'id')


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ('project_id', 'role', 'id')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('project_id', 'author_user_id',
                            'created_time', 'id')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author_user_id', 'issue_id',
                            'created_time', 'id')
