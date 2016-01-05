$(document).ready(function() {
	// set up material nav
	$(".button-collapse").sideNav();

	$.ajaxSetup({ 
   	  beforeSend: function(xhr, settings) {
        	 function getCookie(name) {
 	            var cookieValue = null;
        	     if (document.cookie && document.cookie != '') {
            	     var cookies = document.cookie.split(';');
      	             for (var i = 0; i < cookies.length; i++) {
        	             var cookie = jQuery.trim(cookies[i]);
                  	   // Does this cookie string begin with the name we want?
               		      if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             	 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             	 break;
                    	       }
                       }
             	     }
            	      return cookieValue;
        	 }
        	 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            	 // Only send the token to relative URLs i.e. locally.
          	   xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       		  }
    	 } 
	});
	
	var pending_invite_div = $('#invite_table');
	var i = $('#invite_table tr').size() + 1;

	$('#send_invite').click(function(){
		console.log("send invite is working!");
		console.log($('#invite_email').val());
		//pending_invite__div.append("hello");
		$.ajax({
			url : "send_invite/",
			type : "POST",
			data : {invite_email : $('#invite_email').val() },
			success : function(json) {
				if (json['status'] == '1') {
					// add pending invite
					pending_invite_div.append('<tr><td>'+$('#invite_email').val()+'</td></tr>');
					i++;
					// remove text
					$('#invite_email').val('');
					console.log(json);
					console.log("success");
								} else {
					alert("Email send failed!");
				}
			},
			
			error : function(xhr, errmsg, err) {
				alert(errmsg);
				console.log(xhr.status + ":" + xhr.responseText);
			}
		});
	});

	$(".btn-pref .btn").click(function () {
    $(".btn-pref .btn").removeClass("btn-primary").addClass("btn-default");
    // $(".tab").addClass("active"); // instead of this do the below 
   	 $(this).removeClass("btn-default").addClass("btn-primary");   
});
});
