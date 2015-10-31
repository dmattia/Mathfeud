$(document).ready(function() {
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
	
	var pending_invite_div = $('#pending_invite');
	var i = $('#pending_invite tr').size() + 1;

	$('#send_invite').click(function(){
		console.log("send invite is working!")
		console.log($('#invite_email').val())
		$.ajax({
			url : "send_invite/",
			type : "POST",
			data : {invite_email : $('#invite_email').val() },

			success : function(json) {
				if (json['status'] == '1') {
					$('#invite_email').val(''); // remove the text
					console.log(json);
					console.log("success");
					// add pending invite
					pending_invite_div.append('<tr>td>Email:</td> <td>'+invite_email+'</td></tr>');
					i++;
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

});
