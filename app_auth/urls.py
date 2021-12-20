# django imports
from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        views.MyTokenObtainView.as_view(),
        name='token_obtain'
    ),
    path(
        'register/',
        views.CreateUserView.as_view()
    ),
]
