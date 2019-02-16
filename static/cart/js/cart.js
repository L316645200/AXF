$(function () {
    $('.cart').width(innerWidth)
    total()

// 商品 选中 状态
    $('.confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var $that = $(this)

        $.get('/axf/changecartstatus/', {'cartid': cartid}, function (response) {
            // console.log(response)
            var isselect = response['isselect']
            $that.attr('isselect', isselect)
            $that.children().remove()
            if(isselect){
                $that.append('<span class="glyphicon glyphicon-ok"></span>')
            }else {
                $that.append('<span class="no"></span>')
            }
            total()
        })
    })

    // 全选/取消全选
    $('.bill-left .all').click(function () {
        var isall = $(this).attr('isall')
        $(this).children().remove()
        isall = (isall == 'false') ? true : false
        $(this).attr('isall', isall)
        if (isall == true) {
            $(this).append('<span class="glyphicon glyphicon-ok"></span>').append('<b>全选</b>')
        }else {
            $(this).append('<span class="no">').append('<b>全选</b>')
        }

        $.get('/axf/changecartselect/', {'isall': isall}, function (response) {
            if (response['status']==1){
                $('.confirm-wrapper').each(function () {
                    $(this).attr('isselect', isall)
                    $(this).children().remove()
                    if(isall){
                        $(this).append('<span class="glyphicon glyphicon-ok"></span>')
                    }else {
                        $(this).append('<span class="no"></span>')
                    }
                })
                total()
            }
        })
    })


//    计算总数
    function total() {
        var sum = 0
        // 遍历
        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if($confirm.find('.glyphicon-ok').length){
                var price = $content.find('.price').attr('str')
                var num = $content.find('.num').attr('str')
                sum += parseInt(price)*parseInt(num)
            }
        })
        $('.bill .total b').html(sum)
    }

    // 下单
    $('#generate-order').click(function () {
        $.get('/axf/generateorder/', function (response) {
            console.log(response)

            if (response['status']==1){
                var orderid = response['orderid']
                window.open('/axf/orderinfo/?orderid=' + orderid, target='_self')
            }

        })
    })

})