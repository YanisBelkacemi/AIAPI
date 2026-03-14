from django.urls import path
from .import views
#-------------------------#
urlpatterns = [
 path('register' , views.Register.as_view() ),
 path('login' , views.login_view.as_view()),
 path('logout' , views.logout_view.as_view())

]