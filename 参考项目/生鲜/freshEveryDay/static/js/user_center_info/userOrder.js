$(function(){
	var name = $('#name').html();
	{
		if(name)
		{
			$('.login_info').show();
			$('.login_btn').hide();
		}
	}
	//获取a标签的数量,除去上一页和下一页
	var maxNum = $('.pagenation').children('a').length-2;
	var curIndex = parseInt($('#curIndex').html());
	$('#prevPage').bind('click',function(){
		prev(curIndex);
	})
	$('#nextPage').bind('click',function(){
		next(curIndex,maxNum);
	})

	function prev(curIndex)
	{
		if(curIndex>1)
		{
			prevIndex = (curIndex-1);
			gotoUrl = '/user_order/'+prevIndex+'/';
			window.location.href=gotoUrl;
		}
	}

	function next(curIndex,maxNum)
	{
		if(curIndex<maxNum)
		{
			nextIndex = curIndex+1;
			gotoUrl = '/user_order/'+ nextIndex +'/';
			window.location.href=gotoUrl;
		}
	}

})