function data_security() {
    var $password = $('#u_password');
    $password.val(md5(md5($password.val())));
    return true
}

$(function () {
    if($('#u_name') == 0){
        alert(1)
        $('#msg').hide()
    }
})