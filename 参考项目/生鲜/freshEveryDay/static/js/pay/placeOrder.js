$(function(){
	var name=$('#userName').html();
	if(name)
	{
		$('#welcome').show();
		$('#login').hide();
	}
	else
	{
		$('#welcome').hide();
	}
}) 