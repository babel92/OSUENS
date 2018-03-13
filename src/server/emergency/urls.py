from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get$', views.get, name='get'),
    url(r'^add$', views.add, name='add'),
    url(r'^geo$', views.geo, name='geo'),
]
