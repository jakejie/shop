$(function(){
	$('.addressInfo #reli_name').bind('blur',function(){
		var name = $('.form_group #reli_name').val();
		if(!isName(name))
		{
			$('.tooltip1').html('&nbsp;请输入合法的名字');
		}		
	})

	$('.addressInfo #reli_name').bind('click',function(){
			$('.tooltip1').html('');
	})


	$('.addressInfo #postCode').bind('blur',function(){			
		var postCode = $('.form_group #postCode').val(); 
		if(!isPostCode(postCode))
		{
			$('.tooltip2').html('&nbsp;请输入六位数字的邮编');
		}
		
	})

	$('.addressInfo #postCode').bind('click',function(){			
		$('.tooltip2').html('');	
	})

	$('.addressInfo #phone_number').bind('blur',function(){			
		var number = $('.form_group #phone_number').val(); 
		if(!isPhoneNumber(number))
		{
			$('.tooltip3').html('&nbsp;请输入11位数字的手机号');
		}
		
	})	

	$('.addressInfo #phone_number').bind('click',function(){			
		$('.tooltip3').html('');	
	})

	
	function isName(name)
	{
		if(name.length<2 || name.length>5)
		{
			return false;
		}
		else
		{
			return true
		}
	}

	function isPostCode(postCode)
	{
		var pattern = new RegExp("[0-9]{6}");
		return pattern.test(postCode);
	}

	function isPhoneNumber(number)
	{
		var pattern = new RegExp("1[0-9]{10}");
		return pattern.test(number);
	}
	var userName = $('#name').html();
	{
		if(userName)
		{
			$('.login_info').show();
			$('.login_btn').hide();
		}
	}

})