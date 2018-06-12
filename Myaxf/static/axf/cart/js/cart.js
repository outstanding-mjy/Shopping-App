$(function () {

    $('.subShopping').click(function () {
        var $subShopping = $(this);

        var $li = $subShopping.parents('li');
        console.log($li.attr('cartid'));
        var cartid = $li.attr('cartid');
        $.getJSON('/axf/subtocart/',{'cartid':cartid}, function (data) {
            console.log(data);
            if(data['status'] == '200'){
                if(data['goods_num'] == '0'){
                    $li.remove()
                }else {
                    $subShopping.next().html(data['goods_num']);
                }
                $('#total_price').html(data['total_price']);
            }
        })
    })
    $('.addShopping').click(function () {
        $addShopping = $(this);
        $li = $addShopping.parents('li');
        console.log($li.attr('cartid'));
        cartid = $li.attr('cartid');
        $.getJSON('/axf/addtocart/', {'cartid':cartid},function (data) {
            console.log(data);
            if(data['status'] === '200'){
                $addShopping.prev().html(data['goods_num']);
                $('#total_price').html(data['total_price']);
            }

        })
    })

    $('.confirm').click(function () {
        var $confirm = $(this);
        var $li = $confirm.parents('li');
        var cartid = $li.attr('cartid');
        console.log(cartid);
        $.getJSON('/axf/changecartstatus/',{'cartid':cartid},function (data) {
            console.log(data);
            if (data['status'] == '200'){
                if (data['is_select']){
                    $confirm.find('span').find('span').html('√');
                    if(data['is_all_select']){
                        $('.all_select').find('span').find('span').html('√');
                    }
                }else{
                    $confirm.find('span').find('span').html('');
                    $('.all_select>span>span').html('');
                }
                $('#total_price').html(data['total_price']);
            }

        })
    })
    $('.all_select').click(function () {
        selects = []
        unselects = []
        $('.confirm').each(function () {
            var $confirm = $(this);
            var $li = $confirm.parents('li');
            var cartid = $li.attr('cartid');
            console.log(cartid);

            if($confirm.find('span').find('span').html().length === 0){
                unselects.push(cartid);
            }else {
                selects.push(cartid);
            }

        })
        console.log(selects);
        console.log(unselects);
        if (unselects.length === 0){
            $.getJSON('/axf/changecartsstatus/',{'carts':selects.join('#'), 'select':false},function (data) {
                console.log(data);
                if(data['status'] == '200'){
                    $('.confirm>span>span').html('');
                    $('.all_select>span>span').html('');
                    $('#total_price').html(data['total_price']);
                }
            })
        }else {
        //    变成选中
            $.getJSON('/axf/changecartsstatus/', {'carts': unselects.join('#'), 'select':true},function (data) {
                console.log(data)
                if(data['status'] == '200'){
                    $('.all_select>span>span').html('√');
                    $('.confirm>span>span').html('√');
                    $('#total_price').html(data['total_price']);
                }
            })
        }

    })
    $('#make_order').click(function () {
        var select =[];
        $('.confirm>span>span').each(function () {
            if($(this).html().length > 0){
                select.push($(this).parents('li').attr('cartid'))
            }
        })
        if(select.length === 0){
            alert('还没选择商品');
        }else {
            console.log(select);
            $.getJSON('/axf/makeorder/',{'carts':select.join('#')},function (data) {
                console.log(data);
                if(data['status'] === '200'){
                    window.open('/axf/orderdetail/?order_id='+ data['orderid'],target='_self')
                }

            })
        }
    })

})