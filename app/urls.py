from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^home/$', views.home, name='home'), #  首页

    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),

    url(r'^cart/$', views.cart, name='cart'),

    url(r'^mine/$', views.mine, name='mine'),

    url(r'^register/$', views.register, name='register'),

    url(r'^quit/$', views.quit, name='quit'),

    url(r'^login/$', views.login, name='login'),

    url(r'^checkuser/$', views.checkuser, name='checkuser'),

    url(r'^addcart/$', views.addcart, name='addcart'),# 添加到购物车
    url(r'^subcart/$', views.subcart, name='subcart'),# 购物车删减

    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'), # 修改选中状态
    url(r'^changecartselect/$', views.changecartselect, name='changecartselect'),# 全选/取消全选
    url(r'^generateorder/$', views.generateorder, name='generateorder'), # 下单
    url(r'^orderinfo/$', views.orderinfo, name='orderinfo'), # 订单详情
    url(r'^changeorderstatus/$', views.changeorderstatusm, name='changeorderstatus'),   # 修改订单状态


]