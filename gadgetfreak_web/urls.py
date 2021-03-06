from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_view, name="login"),
	url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^profile/$', views.profile, name="profile"),
	url(r'^register/$', views.register, name="register"),
	url(r'^search/$', views.search, name="search"),
	url(r'^device/(?P<device_id>[0-9]+)$', views.device_info, name="device_info"),
	url(r'^device/(?P<device_id>[0-9]+)/forum$', views.device_forum, name="device_forum"),
	url(r'^device/(?P<device_id>[0-9]+)/forum/(?P<topic_id>[0-9]+)$', views.topic, name="topic"),
	url(r'^device/(?P<device_id>[0-9]+)/forum/add$', views.add_topic, name="add_topic"),
	url(r'^device/(?P<device_id>[0-9]+)/edit$', views.device_edit, name="device_edit"),
	url(r'^device/(?P<device_id>[0-9]+)/delete$', views.device_delete, name="device_delete"),
	url(r'^add/$', views.device_add, name="device_add"),
	url(r'^not_authorized/$', views.not_authorized, name="not_authorized")
]
