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

	// firebase code
	var amOnline = new Firebase('https://mathfeud.firebaseio.com/.info/connected');
	//var userId = 0;
 	var currentStatus = "online";

	var userListRef = new Firebase('https://mathfeud.firebaseio.com/presence/');

	var myUserRef = userListRef.push();

	amOnline.on('value', function(snapshot) {
		if (snapshot.val()) {
			myUserRef.onDisconnect().remove();
			//userRef.set(true);

			setUserStatus("online");
		} else {

			setUserStatus(currentStatus);
		}
	});

	function setUserStatus(status) {
		currentStatus = status;

		myUserRef.set({userId: userId, status: status});
	}
	
	userListRef.on("child_added", function(snapshot) {
		var user = snapshot.val();
		$("#"+user.userId).text(user.status);
	});

	userListRef.on("child_removed", function(snapshot) {
		var user = snapshot.val();
		//setUserStatus("away");
		$("#"+user.userId).text("away");
	});

	userListRef.on("child_changed", function(snapshot){
		console.log("An online status was modified")
		var user = snapshot.val();
		$("#"+user.userId).text(user.status);
	});

	// Check an answer for correctness
	$('.quizQuestion').submit(function(event){
		event.preventDefault()
		var formData = $(this).serialize()
		$.ajax({
			url: "/quiz/checkSubmission/",
			type: "POST",
			data: JSON.stringify({
				'formData': formData
			}),
			success: function(response) {
				console.log(response)
				if(response['valid-response'] == 'Yes') {
					Materialize.toast(response['Correct'], 4000);
				} else {
					Materialize.toast("Invalid Response", 4000);
				}
			},
			error: function(xhr, errmsg, err) {
				Materialize.toast("Something went wrong.", 4000);
				console.log(errmsg + ": " + err);
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});
	});
	
	$('div.answer i.vote-up').click(function() {
		var up = 1;
		var answer_id = $(this).attr("value");
		var score_div = $('div.score div.' + answer_id)
		console.log(answer_id);
		//score_div.html(parseInt(score_div.html()) + 1)
		$.ajax({
			url: "/qa/vote/",
			type: "POST",
			data: {'answer_id': answer_id, 'up': '1'},
			success: function(response) {
				console.log(response)
				if(response['valid-response'] == 'Yes') {
					score_div.html(response['score'])
				} else {
					Materialize.toast("Invalid Response", 4000);
				}
			},
			error: function(xhr, errmsg, err) {
				Materialize.toast("Something went wrong.", 4000);
				console.log(errmsg + ": " + err);
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});

	});
	$('div.answer i.vote-down').click(function() {
		var up = 1;
		var answer_id = $(this).attr("value");
		var score_div = $('div.score div.' + answer_id)
		console.log(answer_id);
		//score_div.html(parseInt(score_div.html()) + 1)
		$.ajax({
			url: "/qa/vote/" ,
			type: "POST",
			data: {'answer_id': answer_id, 'up': '0'},
			success: function(response) {
				console.log(response)
				if(response['valid-response'] == 'Yes') {
					score_div.html(response['score'])
				} else {
					Materialize.toast("Invalid Response", 4000);
				}
			},
			error: function(xhr, errmsg, err) {
				Materialize.toast("Something went wrong.", 4000);
				console.log(errmsg + ": " + err);
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});

	});
	$("button.answer_button").click(function(){
		$("div.answer").show()
	});
	var pending_invite_div = $('#invite_table');
	var i = $('#invite_table tr').size() + 1;

	$('#send_invite').click(function(){
		console.log("send invite is working!");
		console.log($('#invite_email').val());
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
					alert(json['result']);
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
