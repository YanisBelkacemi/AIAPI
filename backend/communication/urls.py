from django.urls import path
from .views import ApiKeyCreation , ModelAccess

urlpatterns = [
    path('' , ApiKeyCreation.as_view()),
    path('generate' , ModelAccess.as_view())
]
