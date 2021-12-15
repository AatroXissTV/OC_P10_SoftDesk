from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=108)
    description = models.CharField(max_length=2048)

    # TODO: Add list of choices for type
    type = models.CharField(max_length=108)

    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       related_name='author',
                                       on_delete=models.CASCADE)


class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project,
                                   related_name='contributors',
                                   on_delete=models.CASCADE)

    # TODO: Add list of choices for role
    role = models.CharField(max_length=108)


class Issue(models.Model):
    title = models.CharField(max_length=108)
    desc = models.CharField(max_length=2048)

    # TODO: implement choices for tags
    tag = models.CharField(max_length=108)

    # TODO: implement choices for priority
    priority = models.CharField(max_length=108)

    project_id = models.ForeignKey(to=Project,
                                   on_delete=models.CASCADE)

    # TODO: implement choices for status
    status = models.CharField(max_length=108)

    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=Contributor,
                                         on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue,
                                 on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
