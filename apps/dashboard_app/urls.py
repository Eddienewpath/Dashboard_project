from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signIn),
    url(r'^login$', views.login_user),
    url(r'^signup$', views.signup),
    url(r'^register',views.register_user),
    url(r'^dashboard', views.success),
    url(r'^logout', views.logout),
    url(r'^post_message', views.post_msg, name='post_msg'),
    url(r'^post_comment/(?P<id>\d+)', views.post_comment, name='post_comment')
    # url(r'^add_user$', views.addUser)
]
