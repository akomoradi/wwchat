"""wwbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from authuser.views import *
from authuser import views
from django.conf import settings
from django.conf.urls.static import static
from chatapi import urls
from rules import urls
from allevents import urls
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapi import consumers

websocket_urlpatterns = [
    path('ws/api/', consumers.ChatConsumer.as_asgi()), # New WebSocket URL
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify/', VerifyOTP.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('login/', views.login_view , name='login'),
    path('chat/', include("chatapi.urls")),
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    path('rapi/' , include('rules.urls') ),
    path('ae/' , include('allevents.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns)
})