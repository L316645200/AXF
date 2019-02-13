from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^home/$', views.home, name='home'),

    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),

    url(r'^cart/$', views.cart, name='cart'),

    url(r'^mine/$', views.mine, name='mine'),

    url(r'^register/$', views.register, name='register'),

    url(r'^quit/$', views.quit, name='quit'),

    url(r'^login/$', views.login, name='login'),

    url(r'^checkuser/$', views.checkuser, name='checkuser'),

    url(r'^addcart/$', views.addcart, name='addcart')

]