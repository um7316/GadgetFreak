from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_view, name="login"),
	url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^device/(?P<device_id>[0-9]+)$', views.device_info, name="device_info"),
	url(r'^device/(?P<device_id>[0-9]+)/forum$', views.device_forum, name="device_forum"),
	url(r'^device/(?P<device_id>[0-9]+)/forum/(?P<topic_id>[0-9]+)$', views.topic, name="topic"),
	url(r'^device/(?P<device_id>[0-9]+)/forum/add$', views.add_topic, name="add_topic"),
	url(r'^device/(?P<device_id>[0-9]+)/edit$', views.device_edit, name="device_edit"),
	url(r'^add/$', views.device_add, name="device_add"),
]
