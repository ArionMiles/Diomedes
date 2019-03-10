from django.conf.urls import url, include

from .views import home_view, task_view, about_view, user_profile, edit_task

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^add-movies/$', task_view, name='task_view'),
    url(r'^about/', about_view, name='about'),
    url(r'^accounts/profile/$', user_profile, name='profile'),
    url(r'^edit-movies/(?P<id>\d+)/$', edit_task, name='edit_task')
]