$(function(){

	var error_name = true;
	var error_password = true;
	var error_check_password = true;
	var error_email = true;
	var error_check = false;


	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var $name = $('#user_name').val();
		var re = /^[a-z0-9_]{5,15}$/i;
		if($name == '') {
			$('#user_name').next().html('用户名不能为空').show();
			error_name = true;
		}
		else {
			if(re.test($name)) {
                $.get('/user/register_exist/?user_name=' + $name, function (data) {
                    data0 = JSON.parse(data);
                    if (data0.count == 1) {
                        $('#user_name').next().html('用户名已存在').show();
                        error_name = true;
                    } else {
                        $('#user_name').next().hide();
                        error_name = false;
                    }
                });
            }else {
				$('#user_name').next().html('用户名必须在5到15个字符之间').show();
				error_name = true;
			}
        }
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}

	function check_email(){
		var $email = $('#email').val();
		var re = /^[a-z0-9][\w\.\_]*@[a-z0-9\_]*(\.[a-z]{2,5}){1,2}$/;

		if($email == '') {
			$('#email').next().html('邮箱不能为空').show();
			error_email = true;
		}
		else
		{
			if(re.test($email)) {
                $.get('/user/register_exist/?email=' + $email, function (data) {
                    data1 = JSON.parse(data);
                    if (data1.count == 1) {
                        $('#email').next().html('邮箱已被注册过').show();
                        error_email = true;
                    } else {
                        $('#email').next().hide();
                        error_email = false;
                    }
                });
            }else {
				$('#email').next().html('不是有效的邮箱').show();
				error_email = true;
			}
		}

	}


	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();
		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});
})