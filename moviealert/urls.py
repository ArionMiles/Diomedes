from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from .views import ProfileView, ReminderView, ReminderEditView, AjaxMovieListView, TrendingView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^add-reminder/$', ReminderView.as_view(), name='reminder_view'),
    url(r'^edit-reminder/(?P<id>\d+)$', ReminderEditView.as_view(), name='edit_reminder'),
    url(r'^ajax/movies/$', cache_page(60*15)(AjaxMovieListView.as_view()), name='ajax_movies'),
    url(r'^trending/$', cache_page(60*15)(TrendingView.as_view()), name='trends'),
]