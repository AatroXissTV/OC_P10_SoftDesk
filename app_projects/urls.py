# django imports
from django.urls import path, include

# django rest_framework imports
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# local imports
from . import views

router = DefaultRouter()
router.register(r'users', views.ProjectViewSet)

projects_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project'
)
projects_router.register(
    r'issues',
    views.IssueViewSet,
    base_name='project-issues'
)
projects_router.register(
    r'contributors',
    views.ContributorViewSet,
    base_name='project-contributors'
)

issues_router = routers.NestedSimpleRouter(
    projects_router,
    r'issues',
    lookup='issue'
)
issues_router.register(
    r'comments',
    views.CommentViewSet,
    base_name='issue-comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]
