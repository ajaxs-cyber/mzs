"""
URL configuration for mzs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("stats/", views.stats_page, name="stats"),
    # 用户认证
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    # API
    path("api/messages/", views.get_messages, name="get_messages"),
    path("api/messages/create/", views.create_message, name="create_message"),
    path("api/cases/", views.get_cases, name="get_cases"),
    path("api/survey/submit/", views.submit_survey, name="submit_survey"),
    path("api/track/visit/", views.track_visit, name="track_visit"),
    path("api/track/scroll/", views.track_scroll, name="track_scroll"),
    path("api/track/duration/", views.track_duration, name="track_duration"),
    path("api/stats/", views.get_stats, name="get_stats"),
    path("api/experiment/", views.get_experiment_data, name="get_experiment"),
    path("experiment/", views.experiment_page, name="experiment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
