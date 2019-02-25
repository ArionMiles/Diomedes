from django.conf.urls import url, include

from .views import home_view, task_view, about_view

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^add-movies/$', task_view, name='task_view'),
    url(r'^about/', about_view, name='about'),
]