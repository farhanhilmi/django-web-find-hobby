from django.urls import path
from .views import *
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('/', views.login_page, name='login_page'),
    path('home', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('logout', views.logout_page, name='logout_page'),

    url(r'^list-forum$', views.list_forum, name='list_forum'),
    #     path('list-forum/update/<str:id>',
    #          views.update_forum, name='update_forum_url'),
    url(r'^list-forum/(?P<pk>\d+)/update/$',
        views.update_forum, name='update_forum_url'),

    path('list-forum/detail/<str:id>',
         views.detail_forum, name='detail_forum_url'),
    path('list-forum/detail/like/<str:id>',
         views.likePost, name='like_forum_url'),

    url(r'^list-forum/detail/(?P<pk>\d+)/update-comment/$',
        views.update_comment, name='update_comment_url'),
    path('list-forum/delete-comment',
         views.delete_comment, name='delete_komentar'),

#     path('list-forum/delete',
#          views.deleteForum, name='delete_forum'),

     path('list-forum/hapus', views.deleteForum, name='hapus_forum'),


    path('list-forum/pencarian',
         views.cari_page, name='pencarian_url'),

    # url(r'^list-forum/add/$', views.forum_add, name='forum_add_url'),
    # url(r'^list-forum/(?P<pk>\d+)/update/$',
    #     views.forum_update, name='forum_update_url'),
    # url(r'^list-forum/(?P<pk>\d+)/delete/$',
    #     views.forum_delete, name='forum_delete_url'),

    path('list-event', views.list_event, name='list_event_url'),
     path('list-event/add', views.tambah_event, name='add_event_url'),
    path('list-event/detail/<str:id>',
         views.detail_event, name='detail_event_url'),
     path('list-event/hapus', views.hapus_event, name='hapus_event'),

    url('list-event/detail/update-event',
        views.update_event, name='update_event_url'),
        
    path('list-event/hadir/<str:id>',
         views.hadirEvent, name='hadirEvent'),


    path('profile/<str:username>',
         views.data_profile, name='profile_url'),
    path('profile/<str:pk>',
         views.update_profile, name='update_profile_url'),
]
