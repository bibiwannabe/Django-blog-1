from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index_(\d+)_(\d+)/$',views.index)
]