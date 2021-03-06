"""finalweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from dating import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^verify_email$', views.verify_email),
    url(r'^edit/', views.edit),
    url(r'^resend/', views.resend),
    url(r'^password/', views.password),
    url(r'^discover/', views.DiscoverView.as_view(), name='discover'),
    url(r'^chats/', views.ChatView.as_view(), name='chats'),
    path('user/<int:id>/', views.UserView.as_view(), name='user'),
    path('chat/<int:id>/', views.chat, name='chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }))
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATICFILES_DIRS[0]
    }))
