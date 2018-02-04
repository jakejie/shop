$(function(){
	var name = $('#userName').html();
	if(name.length)
	{
		$('#welcome').show(); 
		$('#login').hide();
	}
	else
	{
		$('#welcome').hide();
	}

	$('#userCenter').bind('click',function(){
		if(!name)
		{
			$(this).attr('href','/login/');
		}
		
	})
	$('#myOrder').bind('click',function(){
		if(!name)
		{
			$(this).attr('href','/login/');
		}		
	})
	$('#cart').bind('click',function(){
		if(!name)
		{
			$(this).attr('href','/login/');
		}		
	})
	$('.cart_name').bind('click',function(){
		if(!name)
		{
			$(this).attr('href','/login/');
		}		
	})

	$('.goods_con .goods_list li a').bind('click',function(){
		var goodsID = $(this).siblings('#goodsID').text()
		$.ajax({
			url: '/saveGoodsID/',
			type: 'POST',
			dataType: 'json',
			data: {'goodsID': goodsID},
		})	
	})
	$('.goods_con .goods_list h4 a').bind('click',function(){
		var goodsID = $(this).parent().siblings('#goodsID').text()
		$.ajax({
			url: '/saveGoodsID/',
			type: 'POST',
			dataType: 'json',
			data: {'goodsID': goodsID},
		})	
	})
})