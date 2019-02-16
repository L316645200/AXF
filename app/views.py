import hashlib
import os
import uuid

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart, Order, OrderGoods


def home(request):
    wheels = Wheel.objects.all()

    navs = Nav.objects.all()

    mustbuys = Mustbuy.objects.all()

    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    mainshows = MainShow.objects.all()

    data = {
        'title': '首页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shopead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows
    }

    return render(request, 'home.html', context=data)


def market(request, categoryid, childid, sortid):
    # 分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史 [typeIndex]
    # 有typeIndex
    # 无typeIndex，默认0
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    print(foodtypes[typeIndex])
    categoryid = foodtypes[typeIndex].typeid

    # 子类
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames  # 对应分类下 子类字符串
    childlist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        obj = {'childname': arr[0], 'childid': arr[1]}
        childlist.append(obj)

    # 商品数据
    # goodslist = Goods.objects.all()[1:10]

    # 根据商品分类 数据过滤
    # print(childid)
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:  # 对应分类
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid)
        if goodslist.exists():
            pass
        else:
            goodslist = Goods.objects.filter(categoryid=categoryid)

    # 排序处理
    if sortid == '1': # 销量优先
        goodslist = goodslist.order_by('-productnum')
    elif sortid == '2': # 价格最低
        goodslist = goodslist.order_by('price')
    elif sortid == '3': # 价格最高
        goodslist = goodslist.order_by('-price')

    ## 购物车数量问题
    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'childlist': childlist,
        'categoryid': categoryid,
        'childid': childid,
        'carts': carts,
    }
    return render(request, 'market.html', context=data)


def cart(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user).exclude(number=0)
    return render(request, 'cart.html', context={'carts':carts})


def mine(request):
    token = request.session.get('token')
    responseData = {
        'title': '个人中心',
        'payed': 0,
        'wait_pay': 0
    }
    if token:
        user = User.objects.get(token=token)
        print(user.name)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True

        # 获取订单信息
        orders = Order.objects.filter(user=user)
        payed = 0  # 已付款
        wait_pay = 0  # 待付款
        for order in orders:
            if order.status == 1:
                wait_pay += 1
            elif order.status == 2:
                payed += 1

        responseData['payed'] = payed
        responseData['wait_pay'] = wait_pay
    else:
        responseData['name'] = '未登录'
        responseData['rank'] = '无等级（未登录）'
        responseData['img'] = '/static/uploads/axf.png'
        responseData['islogin'] = False
    return render(request, 'mine.html', context=responseData)


def register(request):
    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.address = request.POST.get('address')

        # 头像
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT, imgName)
        file = request.FILES.get('file')
        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        # token
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        user.save()

        # session
        request.session['token'] = user.token

        return redirect('axf:mine')

    elif request.method == 'GET':
        return render(request, 'register.html')

def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()


def quit(request):
    # request.session.flush()
    logout(request)
    return redirect('axf:mine')


def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = generate_password(request.POST.get('password'))
        try:
            user = User.objects.get(account=account)
            if user.password != password:
                return render(request, 'login.html', context={'error': '账号或密码错误'})
            else:
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                # 状态保持
                request.session['token'] = user.token
                return redirect('axf:mine')
        except:
            return render(request, 'login.html', context={'error':'账号或密码错误'})

    elif request.method == 'GET':
        return render(request, 'login.html')

def checkuser(request):
    account = request.GET.get('account')
    try:
        user = User.objects.get(account=account)
        return JsonResponse({'msg':'用户名已存在','status':-1})
    except:
        return JsonResponse({'msg':'用户名可用','status':1})


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')
    responseData = {}

    if token:
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number + 1
            if cart.number > goods.storenums:
                cart.number = goods.storenums
            cart.save()

            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)

        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)
    else:
        responseData['msg'] = '未登录'
        responseData['status'] = -1
        return JsonResponse(responseData)


def subcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    goods = Goods.objects.get(pk=goodsid)
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(goods=goods).filter(user=user)
    cart = carts.first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {}
    responseData['msg'] = '删减购物车成功'
    responseData['status'] = 1
    responseData['number'] = cart.number
    return JsonResponse(responseData)


def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    responseData = {
        'msg': '修改购物车状态成功',
        'status': 1,
        'isselect': cart.isselect
    }

    return JsonResponse(responseData)


def changecartselect(request):
    isall = request.GET.get('isall')
    if isall == 'true':
        isall = True
    else:
        isall = False
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isall
        cart.save()

    responseData = {
        'msg': '全选/取消成功',
        'status': 1,
    }
    return JsonResponse(responseData)


def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    ## 生成订单
    order = Order()
    order.user = user
    order.number = str(uuid.uuid5(uuid.uuid4(), 'order'))
    order.save()
    carts = Cart.objects.filter(user=user).filter(isselect=True)
    for cart in carts:
        ordergoods = OrderGoods()
        ordergoods.order = order
        ordergoods.goods = cart.goods
        ordergoods.number = cart.number
        ordergoods.save()
        # 移除购物车
        cart.delete()
        # 销售量增加 库存减少

    responseData = {
        'msg':'订单生成成功（未付款）',
        'status':1,
        'orderid':order.id
    }
    return JsonResponse(responseData)


def orderinfo(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)

    responseData = {
        'title': '订单详情',
        'order': order,
    }

    return render(request, 'orderinfo.html', context=responseData)


def changeorderstatusm(request):
    orderid = request.GET.get('orderid')
    status = request.GET.get('status')

    order = Order.objects.get(pk=orderid)
    order.status = status
    order.save()

    responseData = {
        'msg':'付款成功',
        'status':1
    }

    return JsonResponse(responseData)