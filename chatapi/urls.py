from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("my-messages/<user_id>/", views.MyInbox.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),
    path('users/', views.GetAllUsers.as_view(), name='all-users'),


]