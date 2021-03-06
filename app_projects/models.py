from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

TYPE_CHOICES = (
    ('backend', 'backend'),
    ('frontend', 'frontend'),
    ('ios', 'ios'),
    ('android', 'android'),
)

ROLE_CHOICES = (
    ('author', 'author'),
    ('contributor', 'contributor'),
)

TAG_CHOICES = (
    ('bug', 'bug'),
    ('upgrade', 'upgrade'),
    ('task', 'task'),
)

PRIORITY_CHOICES = (
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high'),
)

STATUS_CHOICES = (
    ('to do', 'to do'),
    ('in progress', 'in progress'),
    ('done', 'done'),
)


class Project(models.Model):
    title = models.CharField(max_length=108)
    description = models.CharField(max_length=2048)
    type = models.CharField(choices=TYPE_CHOICES,
                            max_length=108)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    related_name='author',
                                    on_delete=models.CASCADE)


@receiver(post_save, sender=Project)
def add_contributor(sender, instance, created, **kwargs):
    """
    Add the author as a contributor to the project.
    """
    # check if contributor already exists
    if created:
        Contributor.objects.create(
            user=instance.author_user,
            project=instance,
            role='author'
        )


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project,
                                related_name='contributors',
                                on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES,
                            default='contributor',
                            max_length=108)


class Issue(models.Model):
    title = models.CharField(max_length=108)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(choices=TAG_CHOICES,
                           max_length=108)
    priority = models.CharField(choices=PRIORITY_CHOICES,
                                default='low',
                                max_length=108)
    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='to do',
                              max_length=108)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=Contributor,
                                      on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue,
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
