from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    url(r'^login/$', views.login),
    url(r'^logout/$',views.logout),
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login_handle/$',views.login_handle),
    url(r'^info/$',views.info),
    url(r'^articles_(\d+)_(\d+)/$',views.articles),
    url(r'^userart_(\d+)/$',views.detail),
    url(r'^create/$',views.create_article),
    url(r'^create_handle/$',views.creat_handle),
    url(r'head/$',views.head),
            ]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)