$(function () {
    $('.register').width(innerWidth)
    // 失去焦点
    // 用户名输入完成， 发起ajax请求，验证用户名是否能用
    $('#account').blur(function () {
        console.log($(this).val())
        $.get('/axf/checkuser/', {'account':$(this).val()}, function (response) {
            // console.log(response)
            if(response['status'] == -1){
                $('#accounterr').show()
            }else {
                $('#accounterr').hide()
            }
        })
    })

    $('#password').blur(function () {
        var password = $(this).val()
        if(password.length<6 || password.password>16){
            $('#passworderr').show()
        }else {
            $('#passworderr').hide()
        }

    })

    $('#mypassword').blur(function () {
        var mypassword = $(this).val()
        console.log(mypassword)
        if(mypassword.length<6 || mypassword.password>16 || mypassword != $('#password').val()){
            $('#mypassworderr').show()
        }else {
            $('#mypassworderr').hide()
        }

    })

})