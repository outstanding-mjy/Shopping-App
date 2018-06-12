$(function () {
     $('.addShopping').each(function () {
         var $addShopping = $(this);
         var goodsid = $addShopping.attr('goodsid');
         $.getJSON('/axf/jsonmarket/',{'goodsid':goodsid},function (data) {
             console.log(data);
             // console.log(data['goodsnum']);
             $addShopping.prev().html(data['goodsnum']);
         })


     })








    $('#all_type').click(function () {
        $('#all_type_container').show()
        $('#sort_rule_container').hide()
        $('#sort_rule').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        $(this).find('span').find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    })
    $('#all_type_container').click(function () {
        $(this).hide()
        $('#all_type').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    })
    $('#sort_rule').click(function () {
        $('#sort_rule_container').show()
        $('#all_type_container').hide()
        $('#all_type').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        $(this).find('span').find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    })
    $('#sort_rule_container').click(function () {
        $(this).hide()
        $('#sort_rule').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    })

    $('.addShopping').click(function () {
        var $addShopping = $(this);
        var goodsid = $addShopping.attr('goodsid');
        $.getJSON('/axf/addtocartinmarket/',{'goodsid':goodsid},function (data) {
            console.log(data);

            if (data['status'] == '200'){
                var goods_num = data['goods_num'];
                $addShopping.prev().html(goods_num)


            }else if(data['status'] == '302'){
                window.open('/axf/mine/',target='_self')
            }
        })


    })

    $('.subShopping').click(function () {
      var $subShopping = $(this);
      // alert(1)

        var goodsid = $subShopping.next().next().attr('goodsid');
        console.log(goodsid);
        $.getJSON('/axf/subtocartinmarket/', {'goodsid':goodsid}, function (data) {

            console.log(data);
            if (data['status'] == '200'){

                $subShopping.next().html(data['goods_num']);
            }else if(data['status'] == '302'){
                window.open('/axf/mine/', target='_self')
            }
        })
    })

})