from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    url(r'^login/$', views.login),
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login_handle/$',views.login_handle),
    url(r'^info/$',views.info),
    url(r'^articles_(\d+)/$',views.articles),
            ]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)