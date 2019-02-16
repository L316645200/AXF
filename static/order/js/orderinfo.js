$(function () {
    $('.order').width(innerWidth)


    $('#alipay').click(function () {
        var orderid = $(this).attr('orderid')
        $.get('/axf/changeorderstatus/', {'orderid':orderid, 'status': 2}, function (response) {
            console.log(response)
            window.open('/axf/mine/', target='_self')
        })
    })
})