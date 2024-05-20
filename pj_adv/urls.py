"""pj_adv URL Configuration

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
from django.urls import include, path
from adv import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('adv/', include("adv.urls")),
                  path("admin/", admin.site.urls),
                  path('index/', views.index, name='index'),
                  path('login/', views.login, name='login'),
                  path('register/', views.register, name='register'),
                  path('update/club/', views.update_club, name='update_club'),
                  path('update/adv/', views.update_adv, name='update_adv'),
                  path('comments/', views.comments, name='comments'),
                  path('observe/adv/', views.adv_list, name='observe_adv_list'),
                  path('observe/adv/<str:adv_title>/', views.adv_detail, name='adv_detail'),
                  path('observe/club/', views.club_list, name='observe_club_list'),
                  path('observe/club/<str:club_name>/', views.club_detail, name='club_detail'),
                  path('logout/', views.logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
