$(function () {
    $('#alipay').click(function () {
        // alert('支付宝正在支付');
        var orderid = $(this).attr('orderid');
        console.log(orderid);
        $.get('/axf/alipay/',{'orderid':orderid},function (data) {
            console.log(data);
            if(data['status'] == '200'){
                window.open('/axf/mine/', target='_self');
            }
        },'json')
    })
})