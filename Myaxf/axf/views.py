import uuid

from django.core import serializers
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from axf import order_status
from axf.models import HomeWheel, HomeNav, Foodtype, HomeMustBuy, HomeShop, HomeShow, Goods, UserModel, CartModel, \
    OrderModel, OrderGoods

ALL_TYPE = '0'
ORDER_TOTAL = '0'
PRICE_ASC = '1'
PRICE_DESC = '2'


def home(request):
    wheels = HomeWheel.objects.all()
    navs = HomeNav.objects.all()
    mustbuys = HomeMustBuy.objects.all()
    shops = HomeShop.objects.all()
    shops0_1 = shops[0:1]
    shops1_3 = shops[1:3]
    shops3_7 = shops[3:7]
    shops7_11 = shops[7:11]
    mainshows = HomeShow.objects.all()
    data = {
        'title':'首页',
        'wheels':wheels,
        'navs': navs,
        'mustbuys':mustbuys,
        'shop0_1':shops0_1,
        'shops1_3':shops1_3,
        'shops3_7':shops3_7,
        'shops7_11':shops7_11,
        'mainshows':mainshows
    }
    return render(request, 'home/home.html', context=data)

def market(request):
    return redirect(reverse('axf:marketwidthparmas', kwargs={'categoryid':104749, 'childcid':0, 'order_rule':0}))

def josn_market(request):
    goodsid = request.GET.get('goodsid')
    userid = request.session.get('user_id')
    if not userid:
        goodsnum = 0
    else:
        cartmodels = CartModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        if cartmodels.exists():
            cartmodel = cartmodels.first()
            # cartmodel = CartModel()
            goodsnum = cartmodel.c_goods_num
        else:
            goodsnum = 0

    data = {
        'status':'200',
        'msg':'ok',
        'goodsnum':goodsnum,
    }

    return JsonResponse(data)

def market_width_parmas(request, categoryid, childcid, order_rule):
    foodtypes = Foodtype.objects.all()
    if childcid == ALL_TYPE:
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:
        goodslist = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == PRICE_ASC:
        goodslist = goodslist.order_by('price')
    elif order_rule == PRICE_DESC:
        goodslist = goodslist.order_by('-price')
    foodtype = Foodtype.objects.get(typeid=categoryid)
    childnames = foodtype.childtypenames
    childname_list = childnames.split('#')
    child_type_list = []
    for childname in childname_list:
        child_type_list.append(childname.split(':'))

    userid = request.session.get('user_id')


    if not userid:
        is_login = False
        cartmodels = 0
    else:
        is_login = True
        cartmodels = CartModel.objects.filter(c_user_id=userid)





    data = {
        'title':'闪购',
        'foodtypes':foodtypes,
        'goodslist':goodslist,
        'categoryid':int(categoryid),
        'childtypelist':child_type_list,
        'childcid':childcid,
        'order_rule':order_rule,
        'cartmodels':cartmodels,
        'islogin':is_login,

    }
    return render(request, 'market/market.html', context=data)


def cart(request):
    userid = request.session.get('user_id')
    if not userid:
        return redirect(reverse('axf:userlogin'))
    user = UserModel.objects.get(pk=userid)
    cartmodels = user.cartmodel_set.all()
    is_all_select = True
    total_price = 0
    for cartmodel in cartmodels:
        if not cartmodel.c_goods_select:
            is_all_select = False
        else:
            total_price += cartmodel.c_goods_num * cartmodel.c_goods.price

    data = {
        'title':'购物车',
        'cartmodels':cartmodels,
        'is_all_select':is_all_select,
        'total_price':'{:.2f}'.format(total_price),

    }
    return render(request, 'cart/cart.html', context=data)


def mine(request):
    is_login = False
    user_id = request.session.get('user_id')
    data = {
        'title': '我的',
        'is_login': is_login,
    }
    if user_id:
        is_login = True
        user = UserModel.objects.get(pk=user_id)
        data['is_login'] = is_login
        data['user_icon'] = '/static/upload/'+user.u_icon.url
        data['username'] = user.u_name
        orderdcount = OrderModel.objects.filter(o_user=user).filter(o_status=order_status.orderd).count()

        if orderdcount > 0:
            data['orderdcount'] = orderdcount

        wait_receive_count = OrderModel.objects.filter(o_user=user).filter(o_status=order_status.PAYED).count()
        if wait_receive_count > 0:
            data['wait_receive_count'] = wait_receive_count

    return render(request, 'mine/mine.html', context=data)


def user_register(request):
    if request.method == 'GET':
        data={
            'title':'用户注册'
        }
        return render(request, 'user/user_register.html', context=data)
    elif request.method == 'POST':

        username = request.POST.get('u_name')
        password = request.POST.get('u_password')
        emal = request.POST.get('u_emal')
        icon = request.FILES.get('u_icon')
        user = UserModel()
        user.u_name = username
        user.u_emal = emal
        user.u_icon = icon
        user.set_password(password)
        user.save()
        send_email_learn(username, emal, user.id)
        return redirect(reverse('axf:mine'))


def user_logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def check_user(request):
    username = request.GET.get('u_name')
    users = UserModel.objects.filter(u_name=username)
    data = {
        'status': '200',
        'msg':'ok'
    }
    if users.exists():
        data['status'] = '801'
        data['msg'] = 'already exists'
        return JsonResponse(data)
    else:
        data['msg'] = 'can use'

        return JsonResponse(data)


def check_emal(request):
    emal = request.GET.get('u_emal')
    users = UserModel.objects.filter(u_emal=emal)
    data = {
        'status':'200',
        'msg':'ok'
    }
    if users.exists():
        data['status']='802'
        data['msg'] = 'emal already exists'

    else:
        data['msg'] = 'can use'
    return JsonResponse(data)


def user_login(request):
    if request.method == 'GET':
        msg = request.session.get('msg')
        data = {
            'title':'用户登录',
            'msg':msg,
        }
        return render(request, 'user/user_login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('u_name')
        password = request.POST.get('u_password')
        users = UserModel.objects.filter(u_name=username)



        if users.exists():
            user = users.first()
            if not user.is_active:
                request.session['msg'] = '用户未激活'
                return redirect(reverse('axf:userlogin'))


            if user.check_password(password):

                request.session['user_id'] = user.id

                return redirect(reverse('axf:mine'))
            else:
                request.session['msg'] = '密码错误'
                return redirect(reverse('axf:userlogin'))
        else:
            request.session['msg'] = '用户不存在'
            return redirect(reverse('axf:userlogin'))


def active_user(request):
    user_token = request.GET.get('utoken')
    print(user_token)
    user_id = cache.get(user_token)
    print('****************************************')
    print(user_id)
    cache.delete(user_token)
    if not user_id:
        return HttpResponse('已过期，请重新激活')
    user = UserModel.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return HttpResponse('激活成功')





def send_email_learn(username, email, userid):
    subject = '爱鲜蜂vip激活邮件'
    message = ''
    recipient_list = [email,]
    tmp = loader.get_template('user/user_active.html')
    token = uuid.uuid4()
    cache.set(token, userid, timeout=60*60)
    print(email)

    data = {
        'username':username,
        'active_url':'http://39.106.28.221/axf/activeuser/?utoken=%s' % token,
    }
    html = tmp.render(data)
    send_mail(subject, message, 'zlq93csdn@163.com', recipient_list, html_message=html)


def add_to_cart_inmarket(request):
    goodsid = request.GET.get('goodsid')
    userid = request.session.get('user_id')
    data = {
        'status':'200',
        'msg':'ok'
    }
    if not userid:
        data['status'] = '302'
        data['msg'] = 'not login'

    else:
        goods = Goods.objects.get(pk=goodsid)
        user = UserModel.objects.get(pk=userid)
        cartmodels = CartModel.objects.filter(c_goods=goods).filter(c_user=user)
        # cartmodels = CartModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        if cartmodels.exists():
            cartmodel = cartmodels.first()
            # cartmodel = CartModel()
            cartmodel.c_goods_num = cartmodel.c_goods_num + 1
            cartmodel.save()
        else:
            cartmodel = CartModel()
            cartmodel.c_goods = goods
            cartmodel.c_user=user
            cartmodel.save()
        data['goods_num']=cartmodel.c_goods_num
    data['total_price'] = '{:.2f}'.format(calc_total(request.session.get('user_id')))

    return JsonResponse(data)


def sub_to_cart(request):

    cardid = request.GET.get('cartid')
    cart_model = CartModel.objects.get(pk=cardid)
    data = {
        'status':'200',
        'msg':'ok',
    }
    if cart_model.c_goods_num == 1:
        cart_model.delete()
        data['goods_num'] = 0
    else:
        cart_model.c_goods_num = cart_model.c_goods_num - 1
        cart_model.save()
        data['goods_num'] = cart_model.c_goods_num

    data['total_price'] = '{:.2f}'.format(calc_total(request.session.get('user_id')))
    return JsonResponse(data)

def add_to_cart(request):
    cartid = request.GET.get('cartid')
    cartmodel = CartModel.objects.get(pk=cartid)
    cartmodel.c_goods_num = cartmodel.c_goods_num + 1
    cartmodel.save()
    data = {
        'status': '200',
        'msg':'ok',
        'goods_num':cartmodel.c_goods_num,
        'total_price': '{:.2f}'.format(calc_total(request.session.get('user_id'))),
    }
    return JsonResponse(data)


def sub_to_cart_inmarket(request):
    goodsid = request.GET.get('goodsid')
    userid = request.session.get('user_id')
    data = {
        'status': '200',
        'msg': 'ok'
    }
    if not userid:
        data['status'] = '302'
        data['msg'] = 'not login'

    else:
        goods = Goods.objects.get(pk=goodsid)
        user = UserModel.objects.get(pk=userid)
        cartmodels = CartModel.objects.filter(c_goods=goods).filter(c_user=user)
        # cartmodels = CartModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        if not cartmodels:

            data['goods_num'] = 0
            data['msg'] = 'can use'
        else:
            cartmodel = cartmodels.first()
            # cartmodel = CartModel()
            cartmodel.c_goods_num = cartmodel.c_goods_num - 1
            cartmodel.save()
            if cartmodel.c_goods_num == 0:
                cartmodel.delete()
            data['goods_num'] = cartmodel.c_goods_num
            data['msg'] = 'can use'
        data['total_price'] = '{:.2f}'.format(calc_total(request.session.get('user_id')))


    return JsonResponse(data)


def change_cart_status(request):

    cartid = request.GET.get('cartid')
    cartmodel = CartModel.objects.get(pk=cartid)
    cartmodel.c_goods_select = not cartmodel.c_goods_select
    cartmodel.save()
    is_all_select = True
    userid = request.session.get('user_id')
    cartmodels = CartModel.objects.filter(c_user_id=userid).filter(c_goods_select=False)
    if cartmodels.exists():
        is_all_select = False
    data = {
        'status':'200',
        'msg':'ok',
        'is_select':cartmodel.c_goods_select,
        'is_all_select':is_all_select,
        'total_price':'{:.2f}'.format(calc_total(request.session.get('user_id'))),
    }
    return JsonResponse(data)


def change_carts_status(request):
    carts = request.GET.get('carts')
    carts_list = carts.split('#')
    print(carts_list)
    select = request.GET.get('select')
    print(select)
    print(type(select))

    if select == 'true':
        is_select = True
    else:
        is_select = False
    for cartid in carts_list:
        cartmodel = CartModel.objects.get(pk=cartid)
        cartmodel.c_goods_select=is_select
        cartmodel.save()
    data = {
        'status':'200',
        'msg':'ok',
        'total_price':'{:.2f}'.format(calc_total(request.session.get('user_id'))),

    }
    return JsonResponse(data)

def calc_total(user_id):
   cartmodels = CartModel.objects.filter(c_user_id=user_id).filter(c_goods_select=True)
   total_price = 0
   for cartmodel in cartmodels:
       total_price += cartmodel.c_goods_num * cartmodel.c_goods.price
   # return total_price
   return total_price


def make_order(request):
    carts = request.GET.get('carts')
    cart_list = carts.split('#')
    print(cart_list)
    userid = request.session.get('user_id')
    order = OrderModel()
    order.o_user_id = userid
    order.o_price = '{:.2f}'.format(calc_total(userid))
    order.save()

    for cartid in cart_list:
        cartmodel = CartModel.objects.get(pk=cartid)
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods = cartmodel.c_goods
        ordergoods.o_goods_num = cartmodel.c_goods_num
        ordergoods.save()
        cartmodel.delete()


    data = {
        'status':'200',
        'msg':'ok',
        'orderid':order.id,
    }
    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('order_id')
    order = OrderModel.objects.get(pk=order_id)

    data = {
        'order':order,
    }
    return render(request, 'order/order_detail.html',context=data)


def alipay(request):
    orderid = request.GET.get('orderid')
    print(orderid)
    order = OrderModel.objects.get(pk=orderid)
    order.o_status = order_status.PAYED
    order.save()
    data = {
        'status':'200',
        'msg': 'ok',
        'order.status':order.o_status,
    }
    return JsonResponse(data)


def order_list(request):
    status = request.GET.get('status')
    userid = request.session.get('user_id')
    if not userid:
        return redirect(reverse('axf:mine'))


    order_list = create_order_list(userid,status)
    data = {
        'orderlist':order_list,
        'status':status,
    }

    return render(request, 'order/order_list.html',context=data)

def create_order_list(userid, status):
    if status:
        return OrderModel.objects.filter(o_user_id=userid).filter(o_status=status)
    else:
        return OrderModel.objects.filter(o_user_id=userid)

def change_order_status(request):
    status = request.GET.get('status')
    print(status)
    userid = request.session.get('user_id')

    data = {
        'status':'200',
        'msg':'ok',
    }
    return JsonResponse(data)

