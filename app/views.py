from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods


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
    print(childid)
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
    return render(request, 'mine.html')