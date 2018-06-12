function check_input() {
    var u_name_color = $('#u_name_info').css('color');
    if (u_name_color == 'rgb(255, 0, 0)'){
        console.log('用户名已存在')
        return false
    }
    var u_emal_color = $('#u_emal_info').css('color');
    if(u_emal_color == 'rgb(255, 0, 0)'){
        return false
    }

    var u_password = $('#u_password').val();
    console.log(u_password);
    var u_password_confirm = $('#u_password_confirm').val();
    console.log(u_password_confirm);
    if (u_password === u_password_confirm){
        $('#u_password').val(md5(md5(u_password)));

        return true

    }else {
        return false

    }
}

$(function () {
    $('#u_name').change(function () {

        var username = $(this).val();
        console.log(username);
        $.getJSON('/axf/checkuser/', {'u_name':username}, function (data) {

            if (data['status'] == '200'){
                $('#u_name_info').html('用户名可用').css('color', 'green')
            }else {
                $('#u_name_info').html('用户名已存在').css('color', 'red')
            }

        })
    })
    $('#u_emal').change(function () {
        var emal = $(this).val();
        a = $(this).val().length;
        console.log(a);
        if (a == 0){
            $('#u_emal_info').html('请输入邮箱').css('color', 'red')
            return
        }


        $.getJSON('/axf/checkemal/',{'u_emal':emal},function (data) {
            console.log(data)
            if(data['status'] == '200'){
                $('#u_emal_info').html('邮箱可用').css('color', 'green')
            }else {

                $('#u_emal_info').html('邮箱已存在').css('color', 'red')
            }

        })
    })
    $('#u_password_confirm').change(function () {
        var password_conform = $(this).val();
        var password = $('#u_password').val();
        if (password === password_conform){
            $('#password_conform_info').css('color', 'green').html('密码输入一致')
        }else{
            $('#password_conform_info').css('color', 'red').html('密码输入不一致')
        }
    })
    $('#u_password').change(function () {
         var password_conform = $('#u_password_confirm').val();
        var password = $('#u_password').val();
        if(password_conform == 0){
            return
        }
        if (password === password_conform){
            $('#password_conform_info').css('color', 'green').html('密码输入一致')
        }else{
            $('#password_conform_info').css('color', 'red').html('密码输入不一致')
        }
    })

})