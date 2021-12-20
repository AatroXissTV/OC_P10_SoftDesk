# django imports
from django.urls import path, include

# django rest_framework imports
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# local imports
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

projects_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project'
)
projects_router.register(
    r'issues',
    views.IssueViewSet,
    basename='project-issues'
)
projects_router.register(
    r'contributors',
    views.ContributorViewSet,
    basename='project-contributors'
)

issues_router = routers.NestedSimpleRouter(
    projects_router,
    r'issues',
    lookup='issue'
)
issues_router.register(
    r'comments',
    views.CommentViewSet,
    basename='issue-comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]
