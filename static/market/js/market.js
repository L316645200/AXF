$(function () {

    // 获取下标 typeIndex
    typeIndex = $.cookie('typeIndex')
    // console.log(typeIndex)
    if(typeIndex){  // 存在，对应分类
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 不存在，默认就是热榜
        $('.type-slider .type-item:first').addClass('active')
    }

    // 侧边栏点击处理 (页面会重新加载)
    $('.type-slider .type-item').click(function () {
        // 保存下标
        // console.log($(this).index())
        // 保存下标 cookie
        $.cookie('typeIndex', $(this).index(),{exprires:3, path:'/'})
    })

    // 分类和排序
    var alltypeBt = false
    var sortBt = false
    $('#allBt').click(function () {
        // 取反
        alltypeBt = !alltypeBt

        if (alltypeBt) { //显示
            $('.bounce-view.type-view').show()
            $('#allBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
            sortBt = false
            $('.bounce-view.sort-view').hide()
            $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        } else { // 隐藏
            $('.bounce-view.type-view').hide()
            $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })


    $('#sortBt').click(function () {
        // 取反
        sortBt = !sortBt

        if (sortBt) { //显示
            $('.bounce-view.sort-view').show()
            $('#sortBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
            alltypeBt = false
            $('.bounce-view.type-view').hide()
            $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        } else { // 隐藏
            $('.bounce-view.sort-view').hide()
            $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })

    $('.bounce-view').click(function () {
        alltypeBt = false
        $('.bounce-view.type-view').hide()
        $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        sortBt = false
        $('.bounce-view.sort-view').hide()
        $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    })

    // 默认隐藏购物车减操作
    $('.bt-wrapper>.glyphicon-minus').hide()
    $('.bt-wrapper>.num').hide()

    // 购物车数据不为0， 即显示
    $('.bt-wrapper>.num').each(function () {
        if (parseInt($(this).html())){
            $(this).show()
            $(this).prev().show()
        }

    })

    // 加操作
    $('.glyphicon-plus').click(function () {
        var goodsid = $(this).attr('goodsid')

        var $that = $(this)
        $.get('/axf/addcart/', {'goodsid':goodsid}, function (response) {
            if(response['status'] == -1) {
                console.log(response)
                window.open('/axf/login/', target='_self')
            }else {
                console.log(response)
                $that.prev().html(response['number']).show()
                $that.prev().prev().show()
            }
        })
    })

    // 减操作
    $('.bt-wrapper>.glyphicon-minus').click(function () {
        var goodsid = $(this).attr('goodsid')

        var $that = $(this)
        $.get('/axf/subcart/', {'goodsid':goodsid}, function (response) {
            console.log(1)
            if(parseInt(response['number']) > 0){
                $that.next().html(response['number']).show()
            }else {
                $that.hide()
                $that.next().hide()
            }
        })
    })

})