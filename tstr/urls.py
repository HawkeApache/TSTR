"""tstr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tstr.tstr_app import views


urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^tests', views.users_groups, name='users_groups'),
    url(r'^group/(?P<group_id>\d+)', views.tests_for_group, name='tests_for_group'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # url(r'^questions', views.questions, name='questions'),
    # url(r'^question/(?P<question_id>\d+)', views.question, name='question'),
    url(r'menu', views.menu, name='menu'),
    url(r'^admin/', admin.site.urls),
    url(r'^settings', views.settings, name='settings'),
    url(r'^test/(?P<test_id>[0-9a-f-]+)/(?P<question_id>[0-9a-f-]+)', views.question, name='test'),
    url(r'^end', views.end, name="end"),
    url(r'^finished', views.finished, name='finished'),
    url(r'^closed_for_group/(?P<group_id>\d+)', views.closed_for_group, name='closed_for_group'),
    url(r'^result/(?P<test_id>[0-9a-f-]+)', views.result, name='result')
]

HANDLER404 = views.error404
HANDLER500 = views.error500
