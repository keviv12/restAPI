from django.urls import path,include
from . import views

urlpatterns = [

    path('userdetails/',views.UserdetailsAPI.as_view()),
    path('deleteuser/',views.DeleteUserAPI.as_view()),
    path('login/',views.LoginAPI.as_view()),
    path('logout/',views.LogoutAPI.as_view())


]

