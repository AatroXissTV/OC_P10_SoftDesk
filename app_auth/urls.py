# django imports
from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        views.MyTokenObtainSerializer.as_view(),
        name='token_obtain'
    ),
    path(
        'register/',
        views.CreateUserView.as_view(),
        name='create_user'
    ),
]
