$(function() {
	$('.user_name').bind('blur', function() {
		var name = $(this).html();
		console.log(name);
		$.ajax({
				url: '/registHandler/',
				type: 'POST',
				dataType: json,
				data: {
					'name': name
				},
			})
			.done(function() {
				flag = isExist;
				alert(flag)
			})

	})
})