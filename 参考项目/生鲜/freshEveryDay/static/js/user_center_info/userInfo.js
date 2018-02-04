$(function(){
	var name = $('#name').html();
	if(name) 
	{
		$('.login_info').show();
		$('.login_btn').hide();
		$('.add_goods').click(function(){
		var goodName = $(this).parent().prev().children('.goods_name').text()
		$.ajax({
			url: '/addGoodsHanderler/',
			type: 'POST',
			dataType: 'json',
			data: {'name': goodName},
		})		
	})

	}
	else
	{
		window.location.href="/login/";
	}
})