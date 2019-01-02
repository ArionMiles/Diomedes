from django.conf.urls import url

from .views import TaskView

urlpatterns = [
    url(r'^$', TaskView, name='home')
]