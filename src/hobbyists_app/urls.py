from django.urls import path
from .views import *
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('home', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('logout', views.logout_page, name='logout_page'),

    url(r'^list-forum/$', views.list_forum, name='list_forum'),
    path('list-forum/<int:event_id>/detail/',
         views.detail_forum, name='detail_forum_url'),
    url(r'^list-forum/add/$', views.forum_add, name='forum_add_url'),
    url(r'^list-forum/(?P<pk>\d+)/update/$',
        views.forum_update, name='forum_update_url'),
    url(r'^list-forum/(?P<pk>\d+)/delete/$',
        views.forum_delete, name='forum_delete_url'),

    path('list-event', views.list_event, name='list_event_url'),
    url(r'^list-event/detail/$', views.detail_event, name='detail_event_url'),

]
