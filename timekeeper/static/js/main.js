$('.toggle_collapse').click(function(){
	if (!$(this).parent().siblings('.panel-body').is(':visible')){
		$(this).children('.glyphicon').removeClass('glyphicon-plus').addClass('glyphicon-minus');
		$(this).parent().siblings('.panel-body').slideDown(150);
	} else {
		$(this).children('.glyphicon').removeClass('glyphicon-minus').addClass('glyphicon-plus');
		$(this).parent().siblings('.panel-body').slideUp(150);
	}
});


$('#calendar').calendar();