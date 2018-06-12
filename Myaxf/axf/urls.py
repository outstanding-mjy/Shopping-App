from django.conf.urls import url

from axf import views








urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^jsonmarket/', views.josn_market, name='jsonmarket'),
    url(r'^marketwidthparmas/(?P<categoryid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_width_parmas, name='marketwidthparmas'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^userregister/', views.user_register, name='userregister'),
    url(r'^userlogout/', views.user_logout, name='userlogout'),
    url(r'^checkuser/', views.check_user, name='checkuser'),
    url(r'^checkemal/', views.check_emal, name='checkemal'),
    url(r'^userlogin/', views.user_login, name='userlogin'),
    url(r'^addtocartinmarket/', views.add_to_cart_inmarket, name='addtocartinmarket'),
    url(r'^subtocartinmarket/', views.sub_to_cart_inmarket, name='subtocartinmarket'),
    url(r'^subtocart/', views.sub_to_cart, name='subtocart'),
    url(r'^addtocart/', views.add_to_cart, name='addtocart'),
    url(r'^changecartstatus/', views.change_cart_status, name='changecartstatus'),
    url(r'^changecartsstatus/', views.change_carts_status, name='changecartsstatus'),
    url(r'^makeorder/', views.make_order, name='makeorder'),
    url(r'^orderdetail/', views.order_detail, name='orderdetail'),
    url(r'^alipay/', views.alipay, name='alipay'),
    url(r'^activeuser/', views.active_user, name='activeuser'),
    url(r'^orderlist/', views.order_list, name='orderlist'),
    url(r'^changeorderstatus/', views.change_order_status, name='changeorderstatus'),

]


