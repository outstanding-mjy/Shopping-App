$(function () {
    $('.affirm_receipt').click(function () {

        $.getJSON('/axf/changeorderstatus/',{'status':2},function (data) {
            console.log(data);
        })
    })
})