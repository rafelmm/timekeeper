(function($){
	$.fn.calendar = function(options){
		
		var defaults = {
				
		};
		
		var settings = $.extend({}, defaults, options);
		
		return this.each(function(index, elem){ 
			cal = $.parseJSON($(elem).attr('data-calendar').replace(/'/gi,'"'));
			
			$(elem).html(get_calendar_html(cal));
			
			$('.calendar-day').click(function(){
				$('#selected_day').html($(this).html());
				$('#selected_month').html(cal.month);
				$('#selected').show();
			})
		});
	};
	
	function get_calendar_html(cal){
		var wrapper = $('<div />').addClass('container');
		var external_row = $('<div />').addClass('row');
		wrapper.append(external_row);
		var calendar_external_col = $('<div />').addClass('col-md-8').addClass('col-xs-12');
		external_row.append(calendar_external_col);
		var calendar_header = $('<div />').addClass('row').addClass('calendar-header');
		calendar_external_col.append(calendar_header);
		
		
		new_html= `
			<div class="container">
				<div class="row">
					<div class="col-md-8 col-xs-12">
						<div class="row calendar-header">
							<div class="calendar-col-1" id="calendar-previous"><span class="glyphicon glyphicon-chevron-left"></span></div>
							<div class="calendar-col-5 calendar-month"> ` + cal.month + ' ' + cal.year + `</div>
							<div class="calendar-col-1" id="calendar-next"><span class="glyphicon glyphicon-chevron-right"></span></div>
						</div>
						<div class="row calendar-weekdays">
							<div class="calendar-col-1">Mo</div>
							<div class="calendar-col-1">Tu</div>
							<div class="calendar-col-1">Wd</div>
							<div class="calendar-col-1">Th</div>
							<div class="calendar-col-1">Fr</div>
							<div class="calendar-col-1">Sa</div>
							<div class="calendar-col-1">Su</div>
						</div>
						<div class="calendar-days">
		`;
					
		$.each(cal.days, function(index, sem){
			new_html+='<div class="row">';
			$.each(sem, function(index, day) {
				if (day != 0){
					new_html+='<div class="calendar-col-1 ' + day.state + ' calendar-day">'+ day.number + '</div>'
				}
				else {
					new_html+='<div class="calendar-col-1 noworkingday">&nbsp;</div>'
				}
			});
			new_html+='</div>';
		});
		
		new_html+=`
				</div>
					<div class="calendar-legend">
						<div class="row">
							<h4 class="calendar-col-7">Calendar Legend:</h4>
							<div class="calendar-legend-item">
								<div class="completed"></div><span>completed</span>
							</div>
							<div class="calendar-legend-item">
								<div class="current"></div><span>uncomplete</span>
							</div>
							<div class="calendar-legend-item">
								<div></div><span>current sprint</span>
							</div>
							<div class="calendar-legend-item">
								<div class="closed"></div><span>closed</span>
							</div>
						</div>
					</div>
				</div>
				<div class="col-md-4 col-xs-12">
					<p id="selected" style="display:none">Details for <span id="selected_day">19</span> of <span id="selected_month">January</span>:</p>
				</div>
			</div>
		</div>
		`;
		return new_html;
	}
	
})(jQuery);

