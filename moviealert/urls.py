from django.urls import include, path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from .views import ProfileView, ReminderView, ReminderEditView, AjaxMovieListView, TrendingView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='home.html'), name='home'),
    path(r'accounts/', include('allauth.urls')),
    path(r'about', TemplateView.as_view(template_name="about.html"), name='about'),
    path(r'accounts/profile', ProfileView.as_view(), name='profile'),
    path(r'add-reminder', ReminderView.as_view(), name='reminder_view'),
    path(r'edit-reminder/<int:id>', ReminderEditView.as_view(), name='edit_reminder'),
    path(r'ajax/movies', cache_page(60*15)(AjaxMovieListView.as_view()), name='ajax_movies'),
    path(r'trending', cache_page(60*15)(TrendingView.as_view()), name='trends'),
    path(r'faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
]