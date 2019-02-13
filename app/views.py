import hashlib
import os
import uuid

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User


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

    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'childlist': childlist,
        'categoryid': categoryid,
        'childid': childid,
    }
    return render(request, 'market.html', context=data)


def cart(request):
    return render(request, 'cart.html')


def mine(request):
    token = request.session.get('token')
    responseData = {}
    if token:
        user = User.objects.get(token=token)
        print(user.name)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True
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
    ResponseData = {}
    ResponseData['goodsid'] = token
    ResponseData['token'] = goodsid

    if token:
        pass
    else:
        pass
    return JsonResponse(ResponseData)