from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^index_(\d+)_(\d+)/$',views.index),
    url(r'^search_(\d+)/$',views.search),
    url(r'^article_(\d+)/$',views.detail),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)