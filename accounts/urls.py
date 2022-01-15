from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^details/$', views.account, name='account'),
    url(r'^details/edit_details/(?P<user_id>\d+)/$',
        views.edit_details, name='edit_details'),
    url(r'^details/edit_address/(?P<user_id>\d+)/$',
        views.edit_address, name='edit_address'),
    # url(r'^details/edit_profile/(?P<user_id>\d+)/$',
    #   views.edit_profile, name='edit_profile'),
]
